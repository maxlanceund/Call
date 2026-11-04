package com.maxlance.call

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.layout.*
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.TextFieldValue
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

    var isPaperMode by remember { mutableStateOf(true) }
    var currentFile by remember { mutableStateOf<File?>(null) }
    var isReadOnly by remember { mutableStateOf(true) }
    var textFieldValue by remember { mutableStateOf(TextFieldValue("")) }

    // 游标卡尺状态
    var showRuler by remember { mutableStateOf(false) }
    var rulerText by remember { mutableStateOf("") }
    val rulerFocusRequester = remember { FocusRequester() }

    // 手势累加器
    var totalDrag by remember { mutableStateOf(0f) }

    val bgColor = if (isPaperMode) Color(0xFFF4F1EA) else Color(0xFF0D1117)
    val textColor = if (isPaperMode) Color(0xFF1A1A1A) else Color(0xFFE6EDF3)

    LaunchedEffect(Unit) {
        val files = context.filesDir.listFiles { file -> file.extension == "md" }
        val validFiles = files?.filter { it.length() > 0 }?.sortedByDescending { it.lastModified() }
        if (validFiles?.isNotEmpty() == true) {
            currentFile = validFiles.first()
            textFieldValue = TextFieldValue(currentFile?.readText() ?: "")
        }
    }

    LaunchedEffect(textFieldValue.text) {
        if (!isReadOnly && textFieldValue.text.isNotEmpty()) {
            delay(1000)
            try { currentFile?.writeText(textFieldValue.text) } catch (e: Exception) {}
        }
    }

    LaunchedEffect(isReadOnly) {
        if (!isReadOnly) {
            delay(150)
            focusRequester.requestFocus()
            keyboardController?.show()
        }
    }

    LaunchedEffect(showRuler) {
        if (showRuler) {
            delay(200)
            rulerFocusRequester.requestFocus()
        }
    }

    // 收纳游标卡尺
    fun commitRuler() {
        if (rulerText.isNotBlank()) {
            val prefix = "# " + rulerText.trim() + "\n\n"
            val newText = if (textFieldValue.text.startsWith(prefix)) textFieldValue.text else prefix + textFieldValue.text
            textFieldValue = TextFieldValue(text = newText, selection = TextRange(prefix.length))
        }
        showRuler = false
        rulerText = ""
        keyboardController?.show()
        focusRequester.requestFocus()
    }

    Box(modifier = Modifier.fillMaxSize().background(bgColor)) {
        Column(modifier = Modifier.fillMaxSize().imePadding().padding(24.dp)) {
            // 顶部：日期和主题切换
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date()),
                    color = textColor.copy(alpha = 0.5f),
                    fontSize = 11.sp,
                    fontFamily = FontFamily.Monospace
                )
                Text(
                    text = "◐",
                    color = textColor.copy(alpha = 0.6f),
                    fontSize = 18.sp,
                    modifier = Modifier.clickable { isPaperMode = !isPaperMode }
                )
            }

            // 中间：正文输入区
            Box(modifier = Modifier.fillMaxWidth().weight(1f)) {
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
                            Text("> Start logging...\n(向右滑写大标题)", color = textColor.copy(alpha = 0.2f), fontFamily = FontFamily.Monospace)
                        }
                        innerTextField()
                    }
                )

                // 🚨 手势拦截层
                if (!isReadOnly) {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .pointerInput(Unit) {
                                detectHorizontalDragGestures(
                                    onDragStart = { totalDrag = 0f },
                                    onDragEnd = { totalDrag = 0f }
                                ) { change, dragAmount ->
                                    change.consume() // 吃掉滑动事件
                                    totalDrag += dragAmount
                                    if (totalDrag > 80 && !showRuler) {
                                        showRuler = true
                                        keyboardController?.hide()
                                    }
                                }
                            }
                    )
                }
            }

            // 底部按键区
            Row(modifier = Modifier.fillMaxWidth().padding(top = 16.dp), horizontalArrangement = Arrangement.Center, verticalAlignment = Alignment.CenterVertically) {
                if (isReadOnly) {
                    // 羽毛笔（已经确认图片存在）
                    Image(
                        painter = painterResource(id = R.drawable.my_pen),
                        contentDescription = "New",
                        colorFilter = ColorFilter.tint(textColor.copy(alpha = 0.8f)),
                        modifier = Modifier
                            .size(24.dp)
                            .clickable {
                                currentFile = File(context.filesDir, "${SimpleDateFormat("yyyy-MM-dd_HHmmss", Locale.getDefault()).format(Date())}.md")
                                textFieldValue = TextFieldValue("")
                                isReadOnly = false
                            }
                            .padding(horizontal = 24.dp)
                    )
                } else {
                    // 保存封印
                    Text(
                        text = "Ξ",
                        color = Color(0xFF58A6FF),
                        fontSize = 22.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier
                            .clickable {
                                if (textFieldValue.text.isNotEmpty()) currentFile?.writeText(textFieldValue.text)
                                isReadOnly = true
                                focusManager.clearFocus()
                                keyboardController?.hide()
                            }
                            .padding(horizontal = 24.dp)
                    )
                }
            }
        }

        // 🚨 游标卡尺 UI（从顶部滑入）
        if (showRuler) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(bgColor.copy(alpha = 0.98f))
                    // 点击任何空白处，触发收纳
                    .clickable(
                        interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                        indication = null
                    ) { commitRuler() }
                    .padding(top = 40.dp, bottom = 20.dp, start = 24.dp, end = 24.dp)
            ) {
                Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    // 左侧刻度线
                    Box(modifier = Modifier.height(1.dp).weight(1f).background(textColor.copy(alpha = 0.4f)))
                    // 几何方块标记
                    Text(" ■■ ", color = textColor, fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                    // 输入区
                    BasicTextField(
                        value = rulerText,
                        onValueChange = { rulerText = it },
                        modifier = Modifier.weight(4f).focusRequester(rulerFocusRequester),
                        textStyle = TextStyle(color = textColor, fontSize = 24.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace),
                        cursorBrush = SolidColor(Color(0xFF58A6FF)),
                        decorationBox = { innerTextField ->
                            if (rulerText.isEmpty()) Text(" 大标题...", color = textColor.copy(alpha = 0.2f))
                            innerTextField()
                        }
                    )
                    // 右侧刻度线
                    Box(modifier = Modifier.height(1.dp).weight(1f).background(textColor.copy(alpha = 0.4f)))
                }
                Spacer(modifier = Modifier.height(12.dp))
                // 提示语
                Text("> 点击空白处收纳封印", color = textColor.copy(alpha = 0.3f), fontSize = 10.sp, modifier = Modifier.align(Alignment.CenterHorizontally))
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
