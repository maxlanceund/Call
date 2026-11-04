#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 正在大海捞针，寻找最近的 Call App 打包任务..."
REPO="maxlanceund/Call"

RUN_ID=$(gh run list --repo $REPO --limit 10 --json databaseId,workflowName,status --jq '.[] | select(.workflowName | contains("Bui")) | select(.status == "completed") | .databaseId' | head -n 1)

if [ -z "$RUN_ID" ]; then
    echo "❌ 找不到打包成功的任务，你推代码了吗？或者云端还在跑？"
    exit 1
fi

echo "🔍 锁定打包任务 ID: $RUN_ID"

rm -rf Call-App-Debug
echo "📥 正在拉取安装包..."
# 下载 artifact
if gh run download $RUN_ID --repo $REPO -n Call-App-Debug; then
    # 直接把里面的 apk 拷到 Download
    if [ -f "Call-App-Debug/app-debug.apk" ]; then
        cp "Call-App-Debug/app-debug.apk" /sdcard/Download/Call_New.apk
        echo "=================================================="
        echo "🎉 完美！最新的 APK 已经躺在你手机的 Download 文件夹里了！"
        echo "👉 去文件管理器里找 Call_New.apk 安装吧！"
        echo "=================================================="
    else
        echo "❌ 下载成功，但里面没找到 apk 文件。"
    fi
else
    echo "❌ 糟糕，下载失败了，可能是网络问题。"
fi
