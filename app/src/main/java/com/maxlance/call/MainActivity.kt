package com.maxlance.call

import android.content.Context
import android.content.Intent
import android.graphics.Typeface
import android.media.AudioManager
import android.media.SoundPool
import android.media.ToneGenerator
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.ExperimentalFoundationApi
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

@OptIn(ExperimentalComposeUiApi::class, ExperimentalFoundationApi::class)
@Composable
fun CallApp() {
    val context = LocalContext.current
    val keyboardController = LocalSoftwareKeyboardController.current
    val focusManager = LocalFocusManager.current
    val focusRequester = remember { FocusRequester() }
    val scrollState = rememberScrollState()

    val toneGenerator = remember {
        ToneGenerator(AudioManager.STREAM_MUSIC, 70)
    }

    val soundPool = remember {
        SoundPool.Builder().setMaxStreams(8).build()
    }

    // 打字音效：三个可选
    val soundIds = remember {
        listOf(
            soundPool.load(context, R.raw.typewriter, 1),
            soundPool.load(context, R.raw.typewriter2, 1),
            soundPool.load(context, R.raw.typewriter3, 1)
        )
    }
    val soundNames = listOf("打字机 1", "打字机 2", "打字机 3")

    // 换行音效：单独一个，不进选择器
    val enterSoundId = remember {
        soundPool.load(context, R.raw.enter, 1)
    }

    val prefs = remember { context.getSharedPreferences("call_prefs", Context.MODE_PRIVATE) }
    var currentSoundIndex by remember {
        mutableStateOf(prefs.getInt("sound_index", 0).coerceIn(0, soundIds.size - 1))
    }
    var showSoundPicker by remember { mutableStateOf(false) }

    DisposableEffect(Unit) {
        onDispose {
            toneGenerator.release()
            soundPool.release()
        }
    }

    var isPaperMode by remember { mutableStateOf(prefs.getBoolean("is_paper_mode", true)) }

    val maxFontFamily = remember {
        try {
            val typeface = Typeface.createFromAsset(context.assets, "max_serif.ttf")
            FontFamily(typeface)
        } catch (e: Exception) {
            FontFamily.Monospace
        }
    }

    var isHistoryOpen by remember { mutableStateOf(false) }
    var currentFile by remember { mutableStateOf<File?>(null) }
    var isReadOnly by remember { mutableStateOf(true) }
    var isDraft by remember { mutableStateOf(false) }
    var textFieldValue by remember { mutableStateOf(TextFieldValue("")) }
    var fontSize by remember { mutableStateOf(16.sp) }
    var allLogs by remember { mutableStateOf<List<File>>(emptyList()) }

    var showTitleInput by remember { mutableStateOf(false) }
    var titleInputValue by remember { mutableStateOf("") }
    val titleFocusRequester = remember { FocusRequester() }

    var longPressedFileName by remember { mutableStateOf<String?>(null) }
    var unlockedFiles by remember { mutableStateOf<Set<String>>(emptySet()) }

    val bgColor = if (isPaperMode) Color(0xFFF4F1EA) else Color(0xFF0D1117)
    val textColor = if (isPaperMode) Color(0xFF1A1A1A) else Color(0xFFE6EDF3)

    val visualTransformation = remember(maxFontFamily) {
        object : VisualTransformation {
            override fun filter(text: AnnotatedString): TransformedText {
                val textStr = text.text
                if (!textStr.contains("# ")) return TransformedText(text, OffsetMapping.Identity)

                val transformed = buildAnnotatedString {
                    var originalIndex = 0
                    while (originalIndex < textStr.length) {
                        if (originalIndex + 1 < textStr.length && textStr[originalIndex] == '#' && textStr[originalIndex + 1] == ' ' && (originalIndex == 0 || textStr[originalIndex - 1] == '\n')) {
                            var endOfLine = textStr.indexOf('\n', originalIndex).let { if (it == -1) textStr.length else it }
                            withStyle(style = SpanStyle(fontSize = 19.sp, fontFamily = maxFontFamily)) { append(textStr.substring(originalIndex + 2, endOfLine)) }
                            originalIndex = endOfLine
                        } else { append(textStr[originalIndex]); originalIndex++ }
                    }
                }

                val offsetMapping = object : OffsetMapping {
                    override fun originalToTransformed(offset: Int): Int {
                        var t = 0; var o = 0
                        while (o < textStr.length && o < offset) {
                            if (o + 1 < textStr.length && textStr[o] == '#' && textStr[o + 1] == ' ' && (o == 0 || textStr[o - 1] == '\n')) { o += 2; if (offset <= o) return t } else { t++; o++ }
                        }
                        return t.coerceIn(0, transformed.length)
                    }

                    override fun transformedToOriginal(offset: Int): Int {
                        var t = 0; var o = 0
                        while (o < textStr.length) {
                            if (o + 1 < textStr.length && textStr[o] == '#' && textStr[o + 1] == ' ' && (o == 0 || textStr[o - 1] == '\n')) { o += 2 } else { if (t == offset) return o; t++; o++ }
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
            scrollState.animateScrollTo(scrollState.maxValue)
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
            val currentText = textFieldValue.text
            val lines = currentText.lines().toMutableList()

            if (lines.isNotEmpty() && lines.first().startsWith("# ")) {
                lines[0] = "# ${titleInputValue.trim()}"
                val newText = lines.joinToString("\n")
                textFieldValue = TextFieldValue(text = newText, selection = TextRange(titleInputValue.length + 2))
            } else {
                val newTitle = "# ${titleInputValue.trim()}\n\n"
                textFieldValue = TextFieldValue(text = newTitle + currentText, selection = TextRange(newTitle.length))
            }

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

    if (showSoundPicker) {
        AlertDialog(
            onDismissRequest = { showSoundPicker = false },
            confirmButton = {},
            title = {
                Text("> 打字音效", color = textColor, fontFamily = FontFamily.Monospace, fontSize = 12.sp)
            },
            text = {
                Column {
                    soundNames.forEachIndexed { index, name ->
                        val selected = index == currentSoundIndex
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    currentSoundIndex = index
                                    prefs.edit().putInt("sound_index", index).apply()
                                    soundPool.play(soundIds[index], 1f, 1f, 1, 0, 1f)
                                }
                                .padding(vertical = 14.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = if (selected) "● " else "○ ",
                                color = if (selected) Color(0xFF58A6FF) else textColor.copy(alpha = 0.4f),
                                fontFamily = FontFamily.Monospace,
                                fontSize = 14.sp
                            )
                            Text(
                                text = name,
                                color = if (selected) Color(0xFF58A6FF) else textColor,
                                fontFamily = FontFamily.Monospace,
                                fontSize = 14.sp
                            )
                        }
                    }
                }
            },
            containerColor = bgColor
        )
    }

    if (isHistoryOpen) {
        AlertDialog(
            onDismissRequest = { isHistoryOpen = false; longPressedFileName = null },
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
                        val content = file.readText()
                        val titleMatch = Regex("^# (.*)", RegexOption.MULTILINE).find(content)
                        val title = titleMatch?.groupValues?.get(1)?.trim()
                        val timeStr = if (fileName.contains("_")) {
                            val datePart = fileName.substringBefore("_").replace("-", " ")
                            val timePart = fileName.substringAfter("_").take(4)
                            val formattedTime = if (timePart.length >= 4) "${timePart.substring(0, 2)}:${timePart.substring(2, 4)}" else timePart
                            "$datePart  $formattedTime"
                        } else fileName

                        val isUnlocked = unlockedFiles.contains(file.absolutePath)
                        val isLongPressed = longPressedFileName == file.absolutePath

                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .combinedClickable(
                                    onClick = {
                                        currentFile = file
                                        textFieldValue = TextFieldValue(file.readText())
                                        isReadOnly = !isUnlocked
                                        isDraft = true
                                        isHistoryOpen = false
                                        longPressedFileName = null
                                    },
                                    onLongClick = {
                                        longPressedFileName = if (isLongPressed) null else file.absolutePath
                                    }
                                )
                                .padding(vertical = 12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                if (!title.isNullOrBlank()) {
                                    Text(text = title, color = if (file == currentFile) Color(0xFF58A6FF) else textColor, fontFamily = FontFamily.Monospace, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(text = timeStr, color = textColor.copy(alpha = 0.4f), fontFamily = FontFamily.Monospace, fontSize = 10.sp)
                                } else {
                                    Text(text = timeStr, color = if (file == currentFile) Color(0xFF58A6FF) else textColor.copy(alpha = 0.7f), fontFamily = FontFamily.Monospace, fontSize = 13.sp)
                                }
                            }

                            if (isLongPressed) {
                                Image(
                                    painter = painterResource(id = if (isUnlocked) R.drawable.toggle_on else R.drawable.toggle_off),
                                    contentDescription = "Toggle",
                                    contentScale = ContentScale.Fit,
                                    colorFilter = ColorFilter.tint(textColor.copy(alpha = 0.8f)),
                                    modifier = Modifier
                                        .padding(start = 16.dp)
                                        .size(width = 20.dp, height = 36.dp)
                                        .clickable(
                                            interactionSource = remember { MutableInteractionSource() },
                                            indication = null
                                        ) {
                                            unlockedFiles = if (isUnlocked) {
                                                unlockedFiles - file.absolutePath
                                            } else {
                                                unlockedFiles + file.absolutePath
                                            }
                                        }
                                )
                            }
                        }
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
                    Text("♪", color = textColor.copy(alpha = 0.6f), fontSize = 16.sp, modifier = Modifier.clickable { showSoundPicker = true }.padding(horizontal = 8.dp))
                    Text("-", color = textColor.copy(alpha = 0.6f), fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.clickable { if (fontSize > 12.sp) fontSize = (fontSize.value - 2).sp }.padding(horizontal = 8.dp))
                    Text("+", color = textColor.copy(alpha = 0.6f), fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.clickable { if (fontSize < 32.sp) fontSize = (fontSize.value + 2).sp }.padding(horizontal = 8.dp))
                    Text("◐", color = textColor.copy(alpha = 0.6f), fontSize = 18.sp, modifier = Modifier.clickable {
                        isPaperMode = !isPaperMode
                        prefs.edit().putBoolean("is_paper_mode", isPaperMode).apply()
                    }.padding(start = 12.dp))
                }
            }

            Box(modifier = Modifier.fillMaxWidth().weight(1f)) {
                BasicTextField(
                    value = textFieldValue,
                    onValueChange = { newValue ->
                        if (!isReadOnly) {
                            val oldText = textFieldValue.text
                            val newText = newValue.text
                            if (newText.length > oldText.length) {
                                val newLineCount = newText.count { c -> c == '\n' }
                                val oldLineCount = oldText.count { c -> c == '\n' }
                                if (newLineCount > oldLineCount) {
                                    // 换行：播齿轮声
                                    soundPool.play(enterSoundId, 1f, 1f, 1, 0, 1f)
                                } else if (newValue.composition == null) {
                                    // 普通打字：播选中的打字音
                                    soundPool.play(soundIds[currentSoundIndex], 1f, 1f, 1, 0, 1f)
                                }
                            }
                            textFieldValue = newValue
                        }
                    },
                    readOnly = isReadOnly,
                    modifier = Modifier.fillMaxSize().focusRequester(focusRequester).verticalScroll(scrollState),
                    textStyle = TextStyle(color = textColor, fontSize = fontSize, lineHeight = (fontSize.value * 1.8).sp, fontFamily = maxFontFamily),
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
                            val currentText = textFieldValue.text
                            if (currentText.startsWith("# ")) {
                                titleInputValue = currentText.substringAfter("# ").substringBefore("\n").trim()
                            } else {
                                titleInputValue = ""
                            }
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
                        textStyle = TextStyle(color = textColor, fontSize = 19.sp, fontFamily = maxFontFamily, textAlign = TextAlign.Center),
                        cursorBrush = SolidColor(textColor),
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                        keyboardActions = KeyboardActions(onDone = { commitTitle() }),
                        decorationBox = { innerTextField ->
                            if (titleInputValue.isEmpty()) {
                                Text("> TITLE", color = textColor.copy(alpha = 0.2f), fontFamily = FontFamily.Monospace, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Center)
                            }
                            innerTextField()
                        }
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Box(modifier = Modifier.fillMaxWidth().height(0.5.dp).background(textColor.copy(alpha = 0.2f)))
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
