package com.maxlance.call

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
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
    var isHistoryOpen by remember { mutableStateOf(false) }
    
    var currentFile by remember { mutableStateOf<File?>(null) }
    var isReadOnly by remember { mutableStateOf(true) }
    var text by remember { mutableStateOf("") }
    
    var allLogs by remember { mutableStateOf<List<File>>(emptyList()) }

    fun refreshLogs() {
        val files = context.filesDir.listFiles { file -> file.extension == "md" }
        allLogs = files?.sortedByDescending { it.lastModified() } ?: emptyList()
    }

    LaunchedEffect(Unit) {
        refreshLogs()
        if (allLogs.isNotEmpty()) {
            currentFile = allLogs.first()
            text = currentFile?.readText() ?: ""
            isReadOnly = true
        }
    }

    val bgColor = if (isPaperMode) Color(0xFFF4F1EA) else Color(0xFF0D1117)
    val textColor = if (isPaperMode) Color(0xFF1A1A1A) else Color(0xFFE6EDF3)

    LaunchedEffect(text) {
        if (!isReadOnly && text.isNotEmpty()) {
            delay(1000)
            try { currentFile?.writeText(text) } catch (e: Exception) { e.printStackTrace() }
        }
    }

    DisposableEffect(Unit) {
        onDispose { if (!isReadOnly && text.isNotEmpty()) currentFile?.writeText(text) }
    }

    val displayDate = currentFile?.name?.replace(".md", "")?.substringBefore("_") ?: SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())

    if (isHistoryOpen) {
        AlertDialog(
            onDismissRequest = { isHistoryOpen = false },
            confirmButton = {},
            title = { Text("> LOGS", color = textColor, fontFamily = FontFamily.Monospace) },
            text = {
                LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp)) {
                    // 💥 核心修复1：加上 key，防止 Compose 在删除时发生节点错乱
                    items(allLogs, key = { it.absolutePath }) { file ->
                        val fileName = file.name.replace(".md", "")
                        val displayName = if (fileName.contains("_")) fileName.replace("_", " / ") else "$fileName / 00:00:00"
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = displayName,
                                color = if (file == currentFile) Color(0xFF58A6FF) else textColor.copy(alpha = 0.7f),
                                fontFamily = FontFamily.Monospace,
                                fontSize = 14.sp,
                                modifier = Modifier
                                    .weight(1f)
                                    .clickable {
                                        currentFile = file
                                        text = file.readText()
                                        isReadOnly = true
                                        isHistoryOpen = false
                                    }
                            )
                            
                            Text(
                                text = "[x]",
                                color = textColor.copy(alpha = 0.3f),
                                fontFamily = FontFamily.Monospace,
                                fontSize = 14.sp,
                                modifier = Modifier
                                    .clickable {
                                        // 💥 核心修复2：安全删除逻辑
                                        val wasCurrent = (currentFile == file)
                                        file.delete()
                                        refreshLogs()
                                        
                                        // 如果删掉的是当前正在看的，必须清空状态，防止去读已经消失的文件
                                        if (wasCurrent) {
                                            if (allLogs.isEmpty()) {
                                                currentFile = null
                                                text = ""
                                                isReadOnly = true
                                            } else {
                                                currentFile = allLogs.first()
                                                text = currentFile?.readText() ?: ""
                                                isReadOnly = true
                                            }
                                        }
                                    }
                                    .padding(start = 16.dp, end = 8.dp)
                            )
                        }
                    }
                }
            },
            containerColor = bgColor
        )
    }

    Column(modifier = Modifier.fillMaxSize().background(bgColor).padding(24.dp)) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = displayDate,
                color = textColor.copy(alpha = 0.6f),
                fontSize = 12.sp,
                fontFamily = FontFamily.Monospace,
                modifier = Modifier.clickable { isHistoryOpen = true }
            )
            
            Row {
                // 只有当存在文件，且当前不是输入状态时，才显示新建
                if (isReadOnly) {
                    TextButton(onClick = {
                        val timestamp = SimpleDateFormat("yyyy-MM-dd_HHmmss", Locale.getDefault()).format(Date())
                        val newFile = File(context.filesDir, "$timestamp.md")
                        newFile.createNewFile()
                        currentFile = newFile
                        text = ""
                        isReadOnly = false
                        refreshLogs()
                    }) {
                        Text("[ + NEW ]", color = textColor.copy(alpha = 0.8f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                    }
                }
                
                TextButton(onClick = { isPaperMode = !isPaperMode }) {
                    Text(if (isPaperMode) "TERMINAL" else "PAPER", color = textColor.copy(alpha = 0.6f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))

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
