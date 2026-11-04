#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 正在连接 GitHub 寻找最新打包任务..."
REPO="maxlanceund/Call"
RUN_ID=$(gh run list --repo $REPO --limit 1 --json databaseId --jq '.[0].databaseId')

if [ -z "$RUN_ID" ]; then
    echo "❌ 没找到任务。"
    exit 1
fi

echo "🔍 锁定任务 ID: $RUN_ID"
while true; do
    # 获取任务状态和结果
    RES=$(gh run view $RUN_ID --repo $REPO --json status,conclusion --jq '.status + "|" + .conclusion')
    STATUS=$(echo $RES | cut -d'|' -f1)
    CONCLUSION=$(echo $RES | cut -d'|' -f2)

    if [ "$STATUS" == "completed" ]; then
        if [ "$CONCLUSION" == "success" ]; then
            echo -e "\n✅ 编译成功！开始下载安装包..."
            break
        else
            echo -e "\n❌ 云端编译彻底失败了！别等了，快去检查代码报错！"
            echo "👇 帮你提取最后几条报错日志："
            gh run view $RUN_ID --repo $REPO --log-failed | tail -n 20
            exit 1
        fi
    else
        echo -n "."
        sleep 5
    fi
done

rm -rf Call-App-Debug
echo "📥 正在拉取..."
if gh run download $RUN_ID --repo $REPO -n Call-App-Debug; then
    APK_FILE=$(find Call-App-Debug -name "*.apk" | head -n 1)
    if [ -n "$APK_FILE" ]; then
        cp "$APK_FILE" /sdcard/Download/Call_New.apk
        echo "=================================================="
        echo "🎉 完美！APK 已经塞进 Download 文件夹了！"
        echo "👉 去文件管理器安装吧！"
        echo "=================================================="
    fi
fi
