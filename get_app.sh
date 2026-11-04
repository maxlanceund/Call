#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 正在寻找最新的 Call App 打包任务..."
REPO="maxlanceund/Call"
RUN_ID=$(gh run list --repo $REPO --limit 1 --json databaseId --jq '.[0].databaseId')

if [ -z "$RUN_ID" ]; then
    echo "❌ 找不到任务。"
    exit 1
fi

echo "🔍 锁定任务 ID: $RUN_ID"
while true; do
    RES=$(gh run view $RUN_ID --repo $REPO --json status,conclusion --jq '.status + "|" + .conclusion')
    STATUS=$(echo $RES | cut -d'|' -f1)
    CONCLUSION=$(echo $RES | cut -d'|' -f2)

    if [ "$STATUS" == "completed" ]; then
        if [ "$CONCLUSION" == "success" ]; then
            echo -e "\n✅ 编译成功！开始下载安装包..."
            break
        else
            echo -e "\n❌ 云端编译彻底失败了！"
            exit 1
        fi
    else
        echo -n "."
        sleep 5
    fi
done

rm -rf Call-App-Debug
rm -f *.apk
echo "📥 正在拉取..."
gh run download $RUN_ID --repo $REPO -n Call-App-Debug 2>/dev/null

# 智能寻找，不管是文件夹还是单文件都能抓到
APK_FILE=$(find . -name "*.apk" | head -n 1)
if [ -n "$APK_FILE" ]; then
    cp "$APK_FILE" /sdcard/Download/Call_New.apk
    echo "=================================================="
    echo "🎉 完美！APK 已经塞进 Download 文件夹了！"
    echo "👉 去文件管理器安装 Call_New.apk 吧！"
    echo "=================================================="
else
    echo "❌ 没找到 APK，可能下载被网络切断了。"
fi
