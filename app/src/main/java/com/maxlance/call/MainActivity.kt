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
    
    val today = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())
    val file = File(context.filesDir, "$today.md")
    
    var isReadOnly by remember { mutableStateOf(file.exists()) }
    var text by remember { mutableStateOf(if (file.exists()) file.readText() else "") }

    val bgColor = if (isPaperMode) Color(0xFFF4F1EA) else Color(0xFF0D1117)
    val textColor = if (isPaperMode) Color(0xFF1A1A1A) else Color(0xFFE6EDF3)

    LaunchedEffect(text) {
        if (!isReadOnly && text.isNotEmpty()) {
            delay(1000)
            try { file.writeText(text) } catch (e: Exception) { e.printStackTrace() }
        }
    }

    DisposableEffect(Unit) {
        onDispose { if (!isReadOnly && text.isNotEmpty()) file.writeText(text) }
    }

    Column(modifier = Modifier.fillMaxSize().background(bgColor).padding(24.dp)) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text(text = today, color = textColor.copy(alpha = 0.4f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
            TextButton(onClick = { isPaperMode = !isPaperMode }) {
                Text(if (isPaperMode) "TERMINAL" else "PAPER", color = textColor.copy(alpha = 0.6f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
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
                if (text.isEmpty()) { Text("> Start logging...", color = textColor.copy(alpha = 0.2f), fontFamily = FontFamily.Monospace) }
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
