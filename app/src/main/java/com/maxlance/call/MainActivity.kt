package com.maxlance.call

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.BasicTextField
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
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

enum class TitleMode { NONE, H1, H2 }

@OptIn(ExperimentalComposeUiApi::class)
@Composable
fun CallApp() {
    val context = LocalContext.current
    val keyboardController = LocalSoftwareKeyboardController.current
    val focusManager = LocalFocusManager.current
    val focusRequester = remember { FocusRequester() }
    val scrollState = rememberScrollState()

    var isPaperMode by remember { mutableStateOf(true) }
    var isHistoryOpen by remember { mutableStateOf(false) }
    var currentFile by remember { mutableStateOf<File?>(null) }
    var isReadOnly by remember { mutableStateOf(true) }
    var isDraft by remember { mutableStateOf(false) }
    
    var textFieldValue by remember { mutableStateOf(TextFieldValue("")) }
    var allLogs by remember { mutableStateOf<List<File>>(emptyList()) }

    // 游标卡尺的状态
    var activeTitleMode by remember { mutableStateOf(TitleMode.NONE) }
    var titleInputValue by remember { mutableStateOf("") }
    val titleFocusRequester = remember { FocusRequester() }

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
            isReadOnly = true
            isDraft = false
        }
    }

    val bgColor = if (isPaperMode) Color(0xFFF4F1EA) else Color(0xFF0D1117)
    val textColor = if (isPaperMode) Color(0xFF1A1A1A) else Color(0xFFE6EDF3)
    val rulerLineColor = textColor.copy(alpha = 0.4f)

    LaunchedEffect(textFieldValue.text) {
        if (!isReadOnly && textFieldValue.text.isNotEmpty()) {
            delay(1000)
            try { currentFile?.writeText(textFieldValue.text) } catch (e: Exception) { e.printStackTrace() }
        }
    }

    DisposableEffect(Unit) {
        onDispose {
            if (currentFile != null && textFieldValue.text.isNotEmpty()) {
                try { currentFile?.writeText(textFieldValue.text) } catch (e: Exception) { e.printStackTrace() }
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

    // 当卡尺滑出时，自动获取焦点
    LaunchedEffect(activeTitleMode) {
        if (activeTitleMode != TitleMode.NONE) {
            delay(200)
            titleFocusRequester.requestFocus()
        }
    }

    // 提交标题逻辑（将内容插入到最前面）
    fun commitTitle() {
        if (titleInputValue.isNotBlank()) {
            val prefix = if (activeTitleMode == TitleMode.H1) "# " else "## "
            val newTitleLine = prefix + titleInputValue.trim() + "\n\n"
            val currentText = textFieldValue.text
            // 简单防重复：如果开头已经是这个标题，就不加了
            val cleanText = if(currentText.startsWith(newTitleLine)) currentText else newTitleLine + currentText
            
            textFieldValue = TextFieldValue(
                text = cleanText,
                selection = TextRange(newTitleLine.length)
            )
        }
        activeTitleMode = TitleMode.NONE
        titleInputValue = ""
        keyboardController?.show()
        focusRequester.requestFocus()
    }

    if (isHistoryOpen) {
        AlertDialog(
            onDismissRequest = { isHistoryOpen = false },
            confirmButton = {},
            title = { Text("> L O G S", color = textColor, fontFamily = FontFamily.Monospace, fontSize = 12.sp) },
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
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    currentFile = file
                                    textFieldValue = TextFieldValue(file.readText())
                                    isReadOnly = true
                                    isDraft = false
                                    isHistoryOpen = false
                                }
                                .padding(vertical = 12.dp)
                        )
                    }
                }
            },
            containerColor = bgColor
        )
    }

    Box(modifier = Modifier.fillMaxSize().background(bgColor)) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .imePadding()
                .padding(24.dp)
        ) {
            // 顶部日期区
            Row(
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                val displayDate = currentFile?.name?.replace(".md", "")?.substringBefore("_") ?: SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())
                Text(
                    text = displayDate.replace("-", " "),
                    color = textColor.copy(alpha = 0.5f),
                    fontSize = 11.sp,
                    letterSpacing = 2.sp,
                    fontFamily = FontFamily.Monospace,
                    modifier = Modifier.clickable { isHistoryOpen = true }
                )

                Text(
                    text = "◐",
                    color = textColor.copy(alpha = 0.6f),
                    fontSize = 18.sp,
                    fontFamily = FontFamily.Monospace,
                    modifier = Modifier
                        .clickable { isPaperMode = !isPaperMode }
                        .padding(start = 16.dp, bottom = 4.dp)
                )
            }

            // 正文输入区
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
            ) {
                BasicTextField(
                    value = textFieldValue,
                    onValueChange = { if (!isReadOnly) textFieldValue = it },
                    readOnly = isReadOnly,
                    modifier = Modifier
                        .fillMaxSize()
                        .focusRequester(focusRequester)
                        .verticalScroll(scrollState),
                    textStyle = TextStyle(color = textColor, fontSize = 16.sp, lineHeight = 28.sp, fontFamily = FontFamily.Monospace),
                    cursorBrush = SolidColor(textColor),
                    decorationBox = { innerTextField ->
                        if (textFieldValue.text.isEmpty() && !isReadOnly) {
                            Text("> Start logging...\n(向右滑写大标题，向左滑写小标题)", color = textColor.copy(alpha = 0.2f), fontFamily = FontFamily.Monospace)
                        }
                        innerTextField()
                    }
                )
                // 🚨 手势监听层：捕获左右滑动，避开上下滚动的冲突
                if (!isReadOnly) {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .pointerInput(Unit) {
                                detectHorizontalDragGestures { _, dragAmount ->
                                    // 向右滑：大标题
                                    if (dragAmount > 80 && activeTitleMode == TitleMode.NONE) {
                                        activeTitleMode = TitleMode.H1
                                        keyboardController?.hide()
                                    } 
                                    // 向左滑：小标题
                                    else if (dragAmount < -80 && activeTitleMode == TitleMode.NONE) {
                                        activeTitleMode = TitleMode.H2
                                        keyboardController?.hide()
                                    }
                                }
                            }
                    )
                }
                if (isReadOnly && isDraft) {
                    Box(modifier = Modifier.fillMaxSize().clickable(
                        indication = null,
                        interactionSource = remember { MutableInteractionSource() }
                    ) { isReadOnly = false })
                }
            }

            // 底部操作栏
            Row(
                modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically
            ) {
                if (isReadOnly) {
                    // 🚨 恢复你的羽毛笔 (如果手机里没有my_pen.png，请确保资源存在)
                    Image(
                        painter = painterResource(id = R.drawable.my_pen),
                        contentDescription = "New",
                        colorFilter = ColorFilter.tint(textColor.copy(alpha = 0.8f)),
                        modifier = Modifier
                            .size(24.dp)
                            .clickable {
                                val timestamp = SimpleDateFormat("yyyy-MM-dd_HHmmss", Locale.getDefault()).format(Date())
                                currentFile = File(context.filesDir, "$timestamp.md")
                                textFieldValue = TextFieldValue("")
                                isReadOnly = false
                                isDraft = true
                            }
                            .padding(horizontal = 24.dp)
                    )
                } else {
                    Text("Ξ", color = Color(0xFF58A6FF), fontSize = 22.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace,
                        modifier = Modifier.clickable {
                            if (textFieldValue.text.isNotEmpty()) currentFile?.writeText(textFieldValue.text)
                            isReadOnly = true
                            focusManager.clearFocus()
                            keyboardController?.hide()
                        }.padding(horizontal = 24.dp, vertical = 8.dp))
                }

                if (textFieldValue.text.isNotEmpty()) {
                    Text("·", color = textColor.copy(alpha = 0.3f), fontSize = 18.sp, fontFamily = FontFamily.Monospace)
                    Text("↑", color = textColor.copy(alpha = 0.8f), fontSize = 20.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace,
                        modifier = Modifier.clickable {
                            val shareIntent = Intent().apply {
                                action = Intent.ACTION_SEND
                                putExtra(Intent.EXTRA_TEXT, textFieldValue.text)
                                type = "text/plain"
                            }
                            context.startActivity(Intent.createChooser(shareIntent, "导出 / 分享日记"))
                        }.padding(horizontal = 24.dp, vertical = 8.dp))
                }
            }
        }

        // 🚨 游标卡尺 UI (从顶部滑入)
        AnimatedVisibility(
            visible = activeTitleMode != TitleMode.NONE,
            enter = slideInVertically(initialOffsetY = { -it }) + fadeIn(),
            exit = slideOutVertically(targetOffsetY = { -it }) + fadeOut(),
            modifier = Modifier.align(Alignment.TopCenter)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(bgColor.copy(alpha = 0.98f))
                    .clickable(
                        indication = null,
                        interactionSource = remember { MutableInteractionSource() }
                    ) {
                        // 点击空白处，当做提交处理
                        commitTitle()
                    }
                    .padding(top = 40.dp, bottom = 20.dp, start = 24.dp, end = 24.dp)
            ) {
                // 卡尺的轴线与输入框
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // 左侧极细刻度线
                    Box(modifier = Modifier.height(1.dp).weight(1f).background(rulerLineColor))
                    
                    // 中间的方块标记 (■ 或 ■■)
                    Text(
                        text = if (activeTitleMode == TitleMode.H1) " ■■ " else " ■ ",
                        color = textColor.copy(alpha = 0.6f),
                        fontSize = 12.sp,
                        fontFamily = FontFamily.Monospace
                    )

                    // 标题输入区
                    BasicTextField(
                        value = titleInputValue,
                        onValueChange = { titleInputValue = it },
                        modifier = Modifier
                            .weight(4f)
                            .focusRequester(titleFocusRequester),
                        textStyle = TextStyle(
                            color = textColor, 
                            fontSize = if (activeTitleMode == TitleMode.H1) 24.sp else 18.sp, // 大标题和小标题字号不同
                            fontWeight = FontWeight.Bold,
                            fontFamily = FontFamily.Monospace
                        ),
                        cursorBrush = SolidColor(Color(0xFF58A6FF)), // 极客蓝光标
                        decorationBox = { innerTextField ->
                            if (titleInputValue.isEmpty()) {
                                Text(" 在此处写字...", color = textColor.copy(alpha = 0.2f), fontFamily = FontFamily.Monospace)
                            }
                            innerTextField()
                        }
                    )

                    // 右侧极细刻度线
                    Box(modifier = Modifier.height(1.dp).weight(1f).background(rulerLineColor))
                }
                
                Spacer(modifier = Modifier.height(12.dp))
                
                // 提示用户如何收纳
                Text(
                    text = "> 点击任意空白处收纳封印",
                    color = textColor.copy(alpha = 0.3f),
                    fontSize = 10.sp,
                    fontFamily = FontFamily.Monospace,
                    modifier = Modifier.align(Alignment.CenterHorizontally)
                )
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
