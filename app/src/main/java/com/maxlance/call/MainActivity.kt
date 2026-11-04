package com.maxlance.call

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.style.TextAlign
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
    var isDraft by remember { mutableStateOf(false) }
    var textFieldValue by remember { mutableStateOf(TextFieldValue("")) }
    var fontSize by remember { mutableStateOf(16.sp) }

    // 🚨 标题输入状态
    var showTitleInput by remember { mutableStateOf(false) }
    var titleInputValue by remember { mutableStateOf("") }
    val titleFocusRequester = remember { FocusRequester() }

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

    // 自动保存
    LaunchedEffect(textFieldValue.text) {
        if (!isReadOnly && textFieldValue.text.isNotEmpty()) {
            delay(1000)
            try { currentFile?.writeText(textFieldValue.text) } catch (e: Exception) {}
        }
    }

    // 退出保存
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

    // 🚨 核心：敲下回车，生成居中的“所见即所得”标题
    fun commitTitle() {
        if (titleInputValue.isNotBlank()) {
            // 不使用 # 号，直接用全角空格和换行让它视觉居中
            val newTitle = "\n${titleInputValue.trim()}\n\n"
            val cleanText = newTitle + textFieldValue.text
            textFieldValue = TextFieldValue(text = cleanText)
        }
        showTitleInput = false
        titleInputValue = ""
        keyboardController?.hide()
    }

    Box(modifier = Modifier.fillMaxSize().background(bgColor)) {
        Column(modifier = Modifier.fillMaxSize().imePadding().padding(24.dp)) {
            
            // 顶部 UI（带 - + ◐）
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(SimpleDateFormat("yyyy MM dd", Locale.getDefault()).format(Date()), color = textColor.copy(alpha = 0.5f), fontSize = 11.sp, letterSpacing = 2.sp, fontFamily = FontFamily.Monospace)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(SimpleDateFormat("HH:mm", Locale.getDefault()).format(Date()), color = textColor.copy(alpha = 0.25f), fontSize = 9.sp, fontFamily = FontFamily.Monospace)
                }
                
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("-", color = textColor.copy(alpha = 0.6f), fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.clickable { if (fontSize > 12.sp) fontSize = (fontSize.value - 2).sp }.padding(horizontal = 8.dp))
                    Text("+", color = textColor.copy(alpha = 0.6f), fontSize = 16.sp, fontWeight = FontWeight.Bold, modifier = Modifier.clickable { if (fontSize < 32.sp) fontSize = (fontSize.value + 2).sp }.padding(horizontal = 8.dp))
                    Text("◐", color = textColor.copy(alpha = 0.6f), fontSize = 18.sp, modifier = Modifier.clickable { isPaperMode = !isPaperMode }.padding(start = 12.dp))
                }
            }

            // 正文区
            Box(modifier = Modifier.fillMaxWidth().weight(1f)) {
                BasicTextField(
                    value = textFieldValue,
                    onValueChange = { if (!isReadOnly) textFieldValue = it },
                    readOnly = isReadOnly,
                    modifier = Modifier.fillMaxSize().focusRequester(focusRequester).verticalScroll(scrollState),
                    textStyle = TextStyle(color = textColor, fontSize = fontSize, lineHeight = (fontSize.value * 1.6).sp, fontFamily = FontFamily.Monospace),
                    cursorBrush = SolidColor(textColor),
                    decorationBox = { innerTextField ->
                        if (textFieldValue.text.isEmpty() && !isReadOnly) {
                            Text("> Start logging...", color = textColor.copy(alpha = 0.2f), fontFamily = FontFamily.Monospace)
                        }
                        innerTextField()
                    }
                )

                if (isReadOnly && isDraft) {
                    Box(
                        modifier = Modifier.fillMaxSize().clickable(
                            indication = null,
                            interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() }
                        ) { isReadOnly = false }
                    )
                }
            }

            // 底部 UI
            Row(modifier = Modifier.fillMaxWidth().padding(top = 16.dp), horizontalArrangement = Arrangement.Center, verticalAlignment = Alignment.CenterVertically) {
                if (isReadOnly) {
                    // 标题按钮（你画的神庙）
                    Image(
                        painter = painterResource(id = R.drawable.title_icon),
                        contentDescription = "Title",
                        colorFilter = ColorFilter.tint(textColor.copy(alpha = 0.8f)),
                        modifier = Modifier.size(24.dp).clickable {
                            showTitleInput = true
                        }.padding(horizontal = 16.dp)
                    )
                    
                    Text("·", color = textColor.copy(alpha = 0.3f), fontSize = 18.sp, fontFamily = FontFamily.Monospace)

                    // 羽毛笔按钮
                    Image(
                        painter = painterResource(id = R.drawable.my_pen),
                        contentDescription = "New",
                        colorFilter = ColorFilter.tint(textColor.copy(alpha = 0.8f)),
                        modifier = Modifier.size(24.dp).clickable {
                            currentFile = File(context.filesDir, "${SimpleDateFormat("yyyy-MM-dd_HHmmss", Locale.getDefault()).format(Date())}.md")
                            textFieldValue = TextFieldValue("")
                            isReadOnly = false
                            isDraft = true
                        }.padding(horizontal = 16.dp)
                    )
                } else {
                    // 假保存 Ξ
                    Text("Ξ", color = Color(0xFF58A6FF), fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.clickable {
                        if (textFieldValue.text.isNotEmpty()) currentFile?.writeText(textFieldValue.text)
                        isReadOnly = true
                        focusManager.clearFocus()
                        keyboardController?.hide()
                    }.padding(horizontal = 24.dp))
                }
            }
        }

        // 🚨 标题输入悬浮 UI（只有一条线，无圆角）
        if (showTitleInput) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(bgColor.copy(alpha = 0.95f))
                    .clickable(
                        indication = null,
                        interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() }
                    ) { /* 阻止点击穿透 */ },
                contentAlignment = Alignment.Center
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    BasicTextField(
                        value = titleInputValue,
                        onValueChange = { titleInputValue = it },
                        modifier = Modifier.fillMaxWidth().focusRequester(titleFocusRequester),
                        textStyle = TextStyle(
                            color = textColor, 
                            fontSize = 24.sp, 
                            fontWeight = FontWeight.Bold, 
                            fontFamily = FontFamily.Monospace,
                            textAlign = TextAlign.Center // 🚨 居中输入
                        ),
                        cursorBrush = SolidColor(textColor),
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                        keyboardActions = KeyboardActions(onDone = { commitTitle() }), // 🚨 回车直接封印
                        decorationBox = { innerTextField ->
                            if (titleInputValue.isEmpty()) {
                                Text("标题", color = textColor.copy(alpha = 0.2f), fontFamily = FontFamily.Monospace)
                            }
                            innerTextField()
                        }
                    )
                    // 那条极其优雅的细线
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
