package com.maxlance.call

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
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

    var isPaperMode by remember { mutableStateOf(true) }
    var isHistoryOpen by remember { mutableStateOf(false) }

    var currentFile by remember { mutableStateOf<File?>(null) }
    var isReadOnly by remember { mutableStateOf(true) }
    var text by remember { mutableStateOf("") }
    var isDraft by remember { mutableStateOf(false) }

    // 新增：文字大小状态
    var fontSize by remember { mutableStateOf(16.sp) }

    var allLogs by remember { mutableStateOf<List<File>>(emptyList()) }

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
            text = currentFile?.readText() ?: ""
            isReadOnly = true
            isDraft = false 
        }
    }

    val bgColor = if (isPaperMode) Color(0xFFF4F1EA) else Color(0xFF0D1117)
    val textColor = if (isPaperMode) Color(0xFF1A1A1A) else Color(0xFFE6EDF3)

    LaunchedEffect(text) {
        if (!isReadOnly && text.isNotEmpty()) {
            scrollState.animateScrollTo(scrollState.maxValue)
            delay(1000)
            try { currentFile?.writeText(text) } catch (e: Exception) { e.printStackTrace() }
        }
    }

    DisposableEffect(Unit) {
        onDispose { 
            if (currentFile != null && text.isNotEmpty()) {
                try { currentFile?.writeText(text) } catch (e: Exception) { e.printStackTrace() }
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

    // 修复Bug2：把 isPaperMode 加入 remember 的 key，让颜色随明暗模式刷新
    val displayDateAnnotated = remember(currentFile, isPaperMode) {
        val dateStr = currentFile?.name?.replace(".md", "") ?: SimpleDateFormat("yyyy-MM-dd_HHmmss", Locale.getDefault()).format(Date())
        val datePart = dateStr.substringBefore("_").replace("-", " ")
        val timePart = if (dateStr.contains("_")) {
            val rawTime = dateStr.substringAfter("_")
            if (rawTime.length >= 4) "${rawTime.substring(0, 2)}:${rawTime.substring(2, 4)}" else ""
        } else {
            SimpleDateFormat("HH:mm", Locale.getDefault()).format(Date())
        }

        buildAnnotatedString {
            withStyle(style = SpanStyle(color = textColor.copy(alpha = 0.5f))) {
                append("$datePart  ")
            }
            if (timePart.isNotEmpty()) {
                withStyle(style = SpanStyle(color = textColor.copy(alpha = 0.25f), fontSize = 9.sp)) {
                    append(timePart)
                }
            }
        }
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
                                    text = file.readText()
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

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
            .imePadding() 
            .padding(24.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = displayDateAnnotated,
                fontSize = 11.sp,
                letterSpacing = 2.sp,
                fontFamily = FontFamily.Monospace,
                modifier = Modifier.clickable { isHistoryOpen = true }
            )

            Row(verticalAlignment = Alignment.CenterVertically) {
                // 新增：减小字号按钮
                Text(
                    text = "-",
                    color = textColor.copy(alpha = 0.6f),
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace,
                    modifier = Modifier
                        .clickable { 
                            if (fontSize > 12.sp) fontSize = (fontSize.value - 2).sp 
                        }
                        .padding(horizontal = 8.dp)
                )
                
                // 新增：增大字号按钮
                Text(
                    text = "+",
                    color = textColor.copy(alpha = 0.6f),
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace,
                    modifier = Modifier
                        .clickable { 
                            if (fontSize < 32.sp) fontSize = (fontSize.value + 2).sp 
                        }
                        .padding(horizontal = 8.dp)
                )

                Text(
                    text = "◐",
                    color = textColor.copy(alpha = 0.6f),
                    fontSize = 18.sp,
                    fontFamily = FontFamily.Monospace,
                    modifier = Modifier
                        .clickable { isPaperMode = !isPaperMode }
                        .padding(start = 12.dp, bottom = 2.dp)
                )
            }
        }

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
        ) {
            BasicTextField(
                value = text,
                onValueChange = { if (!isReadOnly) text = it },
                readOnly = isReadOnly,
                // 修复Bug1：移除两侧可能导致光标卡死的隐形留白
                modifier = Modifier
                    .fillMaxSize()
                    .focusRequester(focusRequester)
                    .verticalScroll(scrollState),
                textStyle = TextStyle(
                    color = textColor, 
                    fontSize = fontSize, // 使用动态字号
                    lineHeight = (fontSize.value * 1.6).sp, // 行高跟着字号动态变，保证排版优雅
                    fontFamily = FontFamily.Monospace
                ),
                cursorBrush = SolidColor(textColor),
                decorationBox = { innerTextField ->
                    if (text.isEmpty() && !isReadOnly) {
                        Text("> Start logging...", color = textColor.copy(alpha = 0.2f), fontSize = fontSize, fontFamily = FontFamily.Monospace)
                    }
                    innerTextField()
                }
            )
            
            if (isReadOnly && isDraft) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .clickable(
                            indication = null, 
                            interactionSource = remember { MutableInteractionSource() }
                        ) {
                            isReadOnly = false 
                        }
                )
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (isReadOnly) {
                Text(
                    text = "+",
                    color = textColor.copy(alpha = 0.8f),
                    fontSize = 20.sp, 
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace,
                    modifier = Modifier.clickable {
                        val timestamp = SimpleDateFormat("yyyy-MM-dd_HHmmss", Locale.getDefault()).format(Date())
                        currentFile = File(context.filesDir, "$timestamp.md")
                        text = ""
                        isReadOnly = false
                        isDraft = true 
                    }.padding(horizontal = 24.dp, vertical = 8.dp)
                )
            } else {
                Text(
                    text = "Ξ",
                    color = Color(0xFF58A6FF),
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace,
                    modifier = Modifier.clickable {
                        if (text.isNotEmpty()) currentFile?.writeText(text)
                        isReadOnly = true 
                        focusManager.clearFocus() 
                        keyboardController?.hide() 
                    }.padding(horizontal = 24.dp, vertical = 8.dp)
                )
            }

            if (text.isNotEmpty()) {
                Text("·", color = textColor.copy(alpha = 0.3f), fontSize = 18.sp, fontFamily = FontFamily.Monospace)
                
                Text(
                    text = "↑",
                    color = textColor.copy(alpha = 0.8f),
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace,
                    modifier = Modifier.clickable {
                        val shareIntent = Intent().apply {
                            action = Intent.ACTION_SEND
                            putExtra(Intent.EXTRA_TEXT, text)
                            type = "text/plain"
                        }
                        context.startActivity(Intent.createChooser(shareIntent, "导出 / 分享日记"))
                    }.padding(horizontal = 24.dp, vertical = 8.dp)
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
