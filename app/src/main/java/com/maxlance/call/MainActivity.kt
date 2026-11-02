package com.maxlance.call

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun CallApp() {
    val context = LocalContext.current
    var isPaperMode by remember { mutableStateOf(true) }
    
    // 当前的日志文件
    var currentFile by remember { mutableStateOf<File?>(null) }
    var isReadOnly by remember { mutableStateOf(true) }
    var text by remember { mutableStateOf("") }

    // 页面加载时，自动显示最新的一篇旧日记（如果有的话）
    LaunchedEffect(Unit) {
        val files = context.filesDir.listFiles { file -> file.extension == "md" }
        if (!files.isNullOrEmpty()) {
            val latestFile = files.maxByOrNull { it.lastModified() }
            if (latestFile != null) {
                currentFile = latestFile
                text = latestFile.readText()
                isReadOnly = true // 旧日记永远只读
            }
        }
    }

    val bgColor = if (isPaperMode) Color(0xFFF4F1EA) else Color(0xFF0D1117)
    val textColor = if (isPaperMode) Color(0xFF1A1A1A) else Color(0xFFE6EDF3)

    // 无感保存逻辑
    LaunchedEffect(text) {
        if (!isReadOnly && text.isNotEmpty()) {
            delay(1000)
            try { currentFile?.writeText(text) } catch (e: Exception) { e.printStackTrace() }
        }
    }

    DisposableEffect(Unit) {
        onDispose { if (!isReadOnly && text.isNotEmpty()) currentFile?.writeText(text) }
    }

    // 格式化时间用于显示和文件名
    val dateFormat = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
    val timeFormat = SimpleDateFormat("HH:mm:ss", Locale.getDefault())
    val currentDate = dateFormat.format(Date())

    Column(modifier = Modifier.fillMaxSize().background(bgColor).padding(24.dp)) {
        // 极简顶栏：日期 + 新建按钮 + 模式切换
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text(text = currentDate, color = textColor.copy(alpha = 0.4f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
            
            Row {
                // 【核心更新】新建切片按钮
                if (isReadOnly) {
                    TextButton(onClick = {
                        // 生成精确到秒的新文件
                        val timestamp = SimpleDateFormat("yyyy-MM-dd_HHmmss", Locale.getDefault()).format(Date())
                        val newFile = File(context.filesDir, "$timestamp.md")
                        newFile.createNewFile()
                        currentFile = newFile
                        text = ""
                        isReadOnly = false // 解除封印，允许输入
                    }) {
                        Text("[ + NEW ]", color = textColor.copy(alpha = 0.8f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                    }
                }
                
                // 模式切换
                TextButton(onClick = { isPaperMode = !isPaperMode }) {
                    Text(if (isPaperMode) "TERMINAL" else "PAPER", color = textColor.copy(alpha = 0.6f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))

        // 核心输入/阅读区
        BasicTextField(
            value = text,
            onValueChange = { if (!isReadOnly) text = it },
            readOnly = isReadOnly,
            modifier = Modifier.fillMaxSize(),
            textStyle = TextStyle(color = textColor, fontSize = 16.sp, lineHeight = 28.sp, fontFamily = FontFamily.Monospace),
            decorationBox = { innerTextField ->
                if (text.isEmpty() && !isReadOnly) {
                    Text("> Start logging...", color = textColor.copy(alpha = 0.2f), fontFamily = FontFamily.Monospace)
                }
                innerTextField()
            }
        )
    }
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { CallApp() }
    }
}
