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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
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
    val focusRequester = remember { FocusRequester() }
    val scrollState = rememberScrollState()

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
            scrollState.animateScrollTo(scrollState.maxValue)
            delay(1000)
            try { currentFile?.writeText(text) } catch (e: Exception) { e.printStackTrace() }
        }
    }

    DisposableEffect(Unit) {
        onDispose { if (!isReadOnly && text.isNotEmpty()) currentFile?.writeText(text) }
    }

    LaunchedEffect(isReadOnly) {
        if (!isReadOnly) {
            delay(100)
            focusRequester.requestFocus()
            keyboardController?.show()
        }
    }

    val displayDate = currentFile?.name?.replace(".md", "")?.substringBefore("_") 
        ?: SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())

    if (isHistoryOpen) {
        AlertDialog(
            onDismissRequest = { isHistoryOpen = false },
            confirmButton = {},
            title = { Text("> LOGS", color = textColor, fontFamily = FontFamily.Monospace) },
            text = {
                LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp)) {
                    items(allLogs, key = { it.absolutePath }) { file ->
                        val fileName = file.name.replace(".md", "")
                        val displayName = if (fileName.contains("_")) fileName.replace("_", " / ") else "$fileName / 00:00:00"
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
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = displayDate,
                color = textColor.copy(alpha = 0.6f),
                fontSize = 12.sp,
                fontFamily = FontFamily.Monospace,
                modifier = Modifier.clickable { isHistoryOpen = true }
            )

            Row {
                if (isReadOnly) {
                    TextButton(onClick = {
                        val timestamp = SimpleDateFormat("yyyy-MM-dd_HHmmss", Locale.getDefault()).format(Date())
                        currentFile = File(context.filesDir, "$timestamp.md")
                        text = ""
                        isReadOnly = false
                    }) {
                        Text("[ + NEW ]", color = textColor.copy(alpha = 0.8f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                    }
                } else {
                    TextButton(onClick = {
                        if (text.isNotEmpty()) currentFile?.writeText(text)
                        isReadOnly = true 
                        keyboardController?.hide() 
                    }) {
                        Text("[ SAVE ]", color = Color(0xFF58A6FF), fontSize = 12.sp, fontFamily = FontFamily.Monospace) 
                    }
                }
                
                if (text.isNotEmpty()) {
                    TextButton(onClick = {
                        val shareIntent = Intent().apply {
                            action = Intent.ACTION_SEND
                            putExtra(Intent.EXTRA_TEXT, text)
                            type = "text/plain"
                        }
                        context.startActivity(Intent.createChooser(shareIntent, "导出 / 分享日记"))
                    }) {
                        Text("[ EXPORT ]", color = textColor.copy(alpha = 0.8f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                    }
                }

                TextButton(onClick = { isPaperMode = !isPaperMode }) {
                    Text(if (isPaperMode) "TERM" else "PAPER", color = textColor.copy(alpha = 0.6f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                }
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .clickable(
                    enabled = isReadOnly, 
                    indication = null, 
                    interactionSource = remember { MutableInteractionSource() }
                ) {
                    isReadOnly = false 
                }
        ) {
            BasicTextField(
                value = text,
                onValueChange = { if (!isReadOnly) text = it },
                readOnly = isReadOnly,
                modifier = Modifier
                    .fillMaxSize()
                    .focusRequester(focusRequester)
                    .verticalScroll(scrollState),
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
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { CallApp() }
    }
}
