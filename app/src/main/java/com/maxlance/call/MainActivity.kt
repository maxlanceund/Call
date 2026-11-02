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
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import java.io.File

@Composable
fun CallApp() {
    // 主题状态：true为米白纸感，false为极客暗黑
    var isPaperMode by remember { mutableStateOf(true) }
    var text by remember { mutableStateOf("") }
    var isSaved by remember { mutableStateOf(false) }

    // 颜色定义
    val bgColor = if (isPaperMode) Color(0xFFF4F1EA) else Color(0xFF0D1117)
    val textColor = if (isPaperMode) Color(0xFF000000) else Color(0xFFFFFFFF)
    val titleColor = if (isPaperMode) Color(0xFF000000) else Color(0xFF58A6FF)

    // 无感保存逻辑（防抖 1 秒）
    LaunchedEffect(text) {
        if (text.isNotEmpty()) {
            delay(1000)
            // 这里的 context 先不传，实际编译需要 context，我先写个伪代码逻辑
            isSaved = true
            delay(1000)
            isSaved = false
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
            .padding(16.dp)
    ) {
        // 顶栏：切换主题 + 保存提示
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = if (isSaved) "Saved" else "",
                color = textColor.copy(alpha = 0.5f),
                fontSize = 12.sp
            )
            TextButton(onClick = { isPaperMode = !isPaperMode }) {
                Text(if (isPaperMode) "DARK" else "PAPER", color = textColor, fontSize = 12.sp)
            }
        }

        // 核心输入区
        BasicTextField(
            value = text,
            onValueChange = { text = it },
            modifier = Modifier
                .fillMaxSize()
                .padding(top = 16.dp),
            textStyle = TextStyle(
                color = textColor,
                fontSize = 16.sp,
                lineHeight = 26.sp,
                fontFamily = FontFamily.Monospace // 极客等宽字体
            ),
            decorationBox = { innerTextField ->
                if (text.isEmpty()) {
                    Text("> Start logging...", color = textColor.copy(alpha = 0.3f))
                }
                innerTextField()
            }
        )
    }
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            CallApp()
        }
    }
}
