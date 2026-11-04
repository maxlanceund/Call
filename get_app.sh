#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 正在寻找最新的 Call App 打包任务..."
REPO="maxlanceund/Call"
RUN_ID=$(gh run list --repo $REPO --workflow "Build Call App" --limit 1 --json databaseId --jq '.[0].databaseId')
if [ -z "$RUN_ID" ]; then
    echo "❌ 找不到打包任务，你推代码了吗？"
    exit 1
fi
echo "🔍 锁定任务 ID: $RUN_ID (云端正在编译中...)"
while true; do
    STATUS=$(gh run view $RUN_ID --repo $REPO --json status --jq '.status')
    if [ "$STATUS" == "completed" ]; then
        echo -e "\n✅ 编译完成，开始下载！"
        break
    fi
    echo -n "."
    sleep 5
done
rm -rf Call-App-Debug
if gh run download $RUN_ID --repo $REPO -n Call-App-Debug; then
    APK_FILE=$(find Call-App-Debug -name "*.apk" | head -n 1)
    if [ -n "$APK_FILE" ]; then
        cp "$APK_FILE" /sdcard/Download/Call_New.apk
        echo "=================================================="
        echo "🎉 完美！全新的 APK 已经塞进 Download 文件夹了！"
        echo "👉 去安装吧，体验你的顶部滑动卡尺 UI！"
        echo "=================================================="
    fi
fi
