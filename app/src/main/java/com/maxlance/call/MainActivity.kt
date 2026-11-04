package com.maxlance.call

import android.content.Intent
import android.graphics.Typeface
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalComposeUiApi::class)
@Composable
fun CallApp() {
    val context = LocalContext.current
    val keyboardController = LocalSoftwareKeyboardController.current
    val focusManager = LocalFocusManager.current
    val focusRequester = remember { FocusRequester() }
    val scrollState = rememberScrollState()

    // 🚨 终极字体加载方案：从 assets 强拽进来，就算天塌下来也能加载！
    val maxFontFamily = remember {
        try {
            val typeface = Typeface.createFromAsset(context.assets, "max_serif.ttf")
            FontFamily(typeface)
        } catch (e: Exception) {
            FontFamily.Monospace // 兜底方案
        }
    }

    var isPaperMode by remember { mutableStateOf(true) }
    var isHistoryOpen by remember { mutableStateOf(false) }
    var currentFile by remember { mutableStateOf<File?>(null) }
    var isReadOnly by remember { mutableStateOf(true) }
    var isDraft by remember { mutableStateOf(false) }
    var textFieldValue by remember { mutableStateOf(TextFieldValue("")) }
    var fontSize by remember { mutableStateOf(16.sp) } // 正文默认 16
    var allLogs by remember { mutableStateOf<List<File>>(emptyList()) }

    var showTitleInput by remember { mutableStateOf(false) }
    var titleInputValue by remember { mutableStateOf("") }
    val titleFocusRequester = remember { FocusRequester() }

    val bgColor = if (isPaperMode) Color(0xFFF4F1EA) else Color(0xFF0D1117)
    val textColor = if (isPaperMode) Color(0xFF1A1A1A) else Color(0xFFE6EDF3)

    // 🚨 终极视觉转换器：19sp，不加粗，使用专属字体
    val visualTransformation = remember(maxFontFamily) {
        object : VisualTransformation {
            override fun filter(text: AnnotatedString): TransformedText {
                val textStr = text.text
                if (!textStr.contains("# ")) return TransformedText(text, OffsetMapping.Identity)

                val transformed = buildAnnotatedString {
                    val lines = textStr.split("\n")
                    for (i in lines.indices) {
                        val line = lines[i]
                        if (line.startsWith("# ")) {
                            // 去掉 FontWeight.Bold，纯靠字体本身的骨骼撑起气势
                            withStyle(style = SpanStyle(fontSize = 19.sp, fontFamily = maxFontFamily)) {
                                append(line.substring(2))
                            }
                        } else {
                            append(line)
                        }
                        if (i < lines.size - 1) append("\n")
                    }
                }

                val offsetMapping = object : OffsetMapping {
                    override fun originalToTransformed(offset: Int): Int {
                        var hiddenCount = 0
                        for (i in 0 until offset) {
                            if (i + 1 < textStr.length && textStr[i] == '#' && textStr[i + 1] == ' ' && (i == 0 || textStr[i - 1] == '\n')) {
                                if (offset <= i + 2) hiddenCount += offset - i else hiddenCount += 2
                            }
                        }
                        return (offset - hiddenCount).coerceIn(0, transformed.length)
                    }
                    override fun transformedToOriginal(offset: Int): Int {
                        if (offset == 0) return 0
                        var transformedCount = 0
                        var originalIndex = 0
                        while (originalIndex < textStr.length) {
                            if (originalIndex + 1 < textStr.length && textStr[originalIndex] == '#' && textStr[originalIndex + 1] == ' ' && (originalIndex == 0 || textStr[originalIndex - 1] == '\n')) {
                                originalIndex += 2
                            } else {
                                transformedCount++
                                originalIndex++
                                if (transformedCount == offset) return originalIndex
                            }
                        }
                        return textStr.length
                    }
                }
                return TransformedText(transformed, offsetMapping)
            }
        }
    }

    fun refreshLogs() {
        val files = context.filesDir.listFiles { file -> file.extension == "md" }
        files?.forEach { if (it.length() == 0L) it.delete() }
        val validFiles = context.filesDir.listFiles { file -> file.extension == "md" }
        allLogs = validFiles?.sortedByDescending { it.lastModified() } ?: emptyList()
    }

    LaunchedEffect(Unit) {
        refreshLogs()
        if (allLogs.isNotEmpty()) {
            currentFile = allLogs.first()
            textFieldValue = TextFieldValue(currentFile?.readText() ?: "")
        }
    }

    LaunchedEffect(textFieldValue.text) {
        if (!isReadOnly && textFieldValue.text.isNotEmpty()) {
            delay(1000)
            try { currentFile?.writeText(textFieldValue.text) } catch (e: Exception) {}
        }
    }

    DisposableEffect(Unit) {
        onDispose {
            if (currentFile != null && textFieldValue.text.isNotEmpty()) {
                try { currentFile?.writeText(textFieldValue.text) } catch (e: Exception) {}
            }
        }
    }

    LaunchedEffect(isReadOnly) {
        if (!isReadOnly) {
            delay(150)
            focusRequester.requestFocus()
            keyboardController?.show()
        }
    }

    LaunchedEffect(showTitleInput) {
        if (showTitleInput) {
            delay(200)
            titleFocusRequester.requestFocus()
        }
    }

    BackHandler(enabled = showTitleInput) {
        showTitleInput = false
        titleInputValue = ""
        focusManager.clearFocus()
        keyboardController?.hide()
    }

    fun commitTitle() {
        if (titleInputValue.isNotBlank()) {
            val newTitle = "\n\n# ${titleInputValue.trim()}\n\n"
            val cleanText = newTitle + textFieldValue.text
            textFieldValue = TextFieldValue(text = cleanText, selection = TextRange(newTitle.length))
            isReadOnly = false
            isDraft = true
            if (currentFile == null) {
                currentFile = File(context.filesDir, "${SimpleDateFormat("yyyy-MM-dd_HHmmss", Locale.getDefault()).format(Date())}.md")
            }
            try { currentFile?.writeText(textFieldValue.text) } catch (e: Exception) {}
        }
        showTitleInput = false
        titleInputValue = ""
        keyboardController?.hide()
        focusRequester.requestFocus()
        refreshLogs()
    }

    if (isHistoryOpen) {
        AlertDialog(
            onDismissRequest = { isHistoryOpen = false },
            confirmButton = {},
            title = {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text("> L O G S", color = textColor, fontFamily = FontFamily.Monospace, fontSize = 12.sp)
                    if (textFieldValue.text.isNotEmpty()) {
                        Text("↑", color = Color(0xFF58A6FF), fontSize = 18.sp, fontWeight = FontWeight.Bold, modifier = Modifier.clickable {
                            val shareIntent = Intent().apply {
                                action = Intent.ACTION_SEND
                                putExtra(Intent.EXTRA_TEXT, textFieldValue.text)
                                type = "text/plain"
                            }
                            context.startActivity(Intent.createChooser(shareIntent, "导出 / 分享日记"))
                        }.padding(8.dp))
                    }
                }
            },
            text = {
                LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp)) {
                    items(allLogs, key = { it.absolutePath }) { file ->
                        val fileName = file.name.replace(".md", "")
                        val displayName = if (fileName.contains("_")) {
                            val datePart = fileName.substringBefore("_").replace("-", " ")
                            val timePart = fileName.substringAfter("_").take(4)
                            val formattedTime = if(timePart.length >= 4) "${timePart.substring(0,2)}:${timePart.substring(2,4)}" else timePart
                            "$datePart  $formattedTime"
                        } else "$fileName"

                        Text(
                            text = displayName,
                            color = if (file == currentFile) Color(0xFF58A6FF) else textColor.copy(alpha = 0.7f),
                            fontFamily = FontFamily.Monospace,
                            fontSize = 14.sp,
                            modifier = Modifier.fillMaxWidth().clickable {
                                    currentFile = file
                                    textFieldValue = TextFieldValue(file.readText())
                                    isReadOnly = true
                                    isDraft = false
                                    isHistoryOpen = false
                                }.padding(vertical = 12.dp)
                        )
                    }
                }
            },
            containerColor = bgColor
        )
    }

    Box(modifier = Modifier.fillMaxSize().background(bgColor)) {
        Column(modifier = Modifier.fillMaxSize().imePadding().padding(24.dp)) {
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(SimpleDateFormat("yyyy MM dd", Locale.getDefault()).format(Date()), color = textColor.copy(alpha = 0.5f), fontSize = 11.sp, letterSpacing = 2.sp, fontFamily = FontFamily.Monospace, modifier = Modifier.clickable { isHistoryOpen = true })
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(SimpleDateFormat("HH:mm", Locale.getDefault()).format(Date()), color = textColor.copy(alpha = 0.25f), fontSize = 9.sp, fontFamily = FontFamily.Monospace)
                }
                
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("-", color = textColor.copy(alpha = 0.6f), fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.clickable { if (fontSize > 12.sp) fontSize = (fontSize.value - 2).sp }.padding(horizontal = 8.dp))
                    Text("+", color = textColor.copy(alpha = 0.6f), fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.clickable { if (fontSize < 32.sp) fontSize = (fontSize.value + 2).sp }.padding(horizontal = 8.dp))
                    Text("◐", color = textColor.copy(alpha = 0.6f), fontSize = 18.sp, modifier = Modifier.clickable { isPaperMode = !isPaperMode }.padding(start = 12.dp))
                }
            }

            Box(modifier = Modifier.fillMaxWidth().weight(1f)) {
                BasicTextField(
                    value = textFieldValue,
                    onValueChange = { if (!isReadOnly) textFieldValue = it },
                    readOnly = isReadOnly,
                    modifier = Modifier.fillMaxSize().focusRequester(focusRequester).verticalScroll(scrollState),
                    // 正文也应用专属字体
                    textStyle = TextStyle(color = textColor, fontSize = fontSize, lineHeight = (fontSize.value * 1.6).sp, fontFamily = maxFontFamily),
                    cursorBrush = SolidColor(textColor),
                    visualTransformation = if (textFieldValue.composition != null) VisualTransformation.None else visualTransformation,
                    decorationBox = { innerTextField ->
                        if (textFieldValue.text.isEmpty() && !isReadOnly) {
                            Text("> Start logging...", color = textColor.copy(alpha = 0.2f), fontFamily = FontFamily.Monospace)
                        }
                        innerTextField()
                    }
                )

                if (isReadOnly && isDraft) {
                    Box(modifier = Modifier.fillMaxSize().clickable(indication = null, interactionSource = remember { MutableInteractionSource() }) { isReadOnly = false })
                }
            }

            Row(modifier = Modifier.fillMaxWidth().padding(top = 16.dp), horizontalArrangement = Arrangement.Center, verticalAlignment = Alignment.CenterVertically) {
                if (isReadOnly) {
                    Image(
                        painter = painterResource(id = R.drawable.my_pen),
                        contentDescription = "New",
                        contentScale = ContentScale.Fit,
                        colorFilter = ColorFilter.tint(textColor.copy(alpha = 0.8f)),
                        modifier = Modifier.padding(horizontal = 24.dp).size(24.dp).clickable {
                            currentFile = File(context.filesDir, "${SimpleDateFormat("yyyy-MM-dd_HHmmss", Locale.getDefault()).format(Date())}.md")
                            textFieldValue = TextFieldValue("")
                            isReadOnly = false
                            isDraft = true
                        }
                    )
                    
                    Text("·", color = textColor.copy(alpha = 0.3f), fontSize = 18.sp, fontFamily = FontFamily.Monospace)

                    Image(
                        painter = painterResource(id = R.drawable.title_icon),
                        contentDescription = "Title",
                        contentScale = ContentScale.Fit,
                        colorFilter = ColorFilter.tint(textColor.copy(alpha = 0.8f)),
                        modifier = Modifier.padding(horizontal = 24.dp).size(24.dp).clickable {
                            showTitleInput = true
                        }
                    )
                } else {
                    Text("Ξ", color = Color(0xFF58A6FF), fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.clickable {
                        if (textFieldValue.text.isNotEmpty()) currentFile?.writeText(textFieldValue.text)
                        isReadOnly = true
                        focusManager.clearFocus()
                        keyboardController?.hide()
                    }.padding(horizontal = 24.dp))
                }
            }
        }

        if (showTitleInput) {
            Box(
                modifier = Modifier.fillMaxSize().background(bgColor.copy(alpha = 0.95f))
                    .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null) { commitTitle() },
                contentAlignment = Alignment.Center
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 32.dp).clickable(interactionSource = remember { MutableInteractionSource() }, indication = null) { },
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    BasicTextField(
                        value = titleInputValue,
                        onValueChange = { titleInputValue = it },
                        modifier = Modifier.fillMaxWidth().focusRequester(titleFocusRequester),
                        // 悬浮标题框也应用 19sp 和专属字体
                        textStyle = TextStyle(color = textColor, fontSize = 19.sp, fontFamily = maxFontFamily, textAlign = TextAlign.Center),
                        cursorBrush = SolidColor(textColor),
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                        keyboardActions = KeyboardActions(onDone = { commitTitle() }),
                        decorationBox = { innerTextField ->
                            if (titleInputValue.isEmpty()) {
                                Text("标题", color = textColor.copy(alpha = 0.2f), fontFamily = FontFamily.Monospace, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Center)
                            }
                            innerTextField()
                        }
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(textColor.copy(alpha = 0.5f)))
                }
            }
        }
    }
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { CallApp() }
    }
}
