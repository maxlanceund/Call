#!/data/data/com.termux/files/usr/bin/bash

REPO="maxlanceund/Call"
ARTIFACT_NAME="Max-Roman-Font"

echo "🚀 1. 正在检查云端最新任务状态..."

# 获取最新的 run ID
RUN_ID=$(gh run list --repo $REPO --workflow "build-font.yml" --limit 1 --json databaseId --jq '.[0].databaseId')

if [ -z "$RUN_ID" ]; then
    echo "❌ 找不到运行记录，你是不是还没推代码上去？"
    exit 1
fi

echo "🔍 锁定任务 ID: $RUN_ID"

# 循环等待云端跑完
while true; do
    STATUS=$(gh run view $RUN_ID --repo $REPO --json status,conclusion --jq '.status')
    CONCLUSION=$(gh run view $RUN_ID --repo $REPO --json status,conclusion --jq '.conclusion')

    if [ "$STATUS" == "completed" ]; then
        if [ "$CONCLUSION" == "success" ]; then
            echo -e "\n✅ 云端跑成功了！正在自动下载字体..."
            break
        else
            echo -e "\n❌ 云端又报错了！(状态: $CONCLUSION)"
            echo "👉 正在拉取报错日志，请查看下方红字："
            gh run view $RUN_ID --repo $REPO --log | grep -A 5 -E "Error|Traceback|Exception"
            exit 1
        fi
    else
        echo -n "."
        sleep 5
    fi
done

# 自动下载 artifact (ZIP包)
echo "📥 正在拉取云端生成的字体包..."
gh run download $RUN_ID --repo $REPO -n $ARTIFACT_NAME

# 此时 Termux 当前目录会多出一个叫 Max-Roman-Font 的文件夹
echo "🗜️ 正在解压并搬运到手机 Download 文件夹..."
unzip -o "$ARTIFACT_NAME/*.zip" -d ./font_out/
cp ./font_out/*.ttf /sdcard/Download/

echo "=================================================="
echo "🎉 完美！你的专属字体已经存到手机 Download 文件夹了！"
echo "👉 去手机文件管理器里找找看，名字应该叫 Max_Font_Cloud.ttf"
echo "=================================================="
