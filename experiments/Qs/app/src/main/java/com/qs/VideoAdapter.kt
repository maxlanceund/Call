package com.qs

import android.content.Context
import android.net.Uri
<<<<<<< HEAD
=======
import android.util.SparseArray
>>>>>>> 501051d231c99e5878bf388804ae80c4f5938d75
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.exoplayer.DefaultRenderersFactory
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import androidx.recyclerview.widget.RecyclerView
import kotlin.math.abs

class VideoAdapter(
    private val context: Context,
    private val videos: List<Uri>,
    private val historyStore: HistoryStore,
    private val onLongPress: () -> Unit
) : RecyclerView.Adapter<VideoAdapter.VH>() {

<<<<<<< HEAD
    // 【核心重构】全场只有一个播放器！不再创建池子！
    private var sharedPlayer: ExoPlayer? = null
=======
    private val playerPool = SparseArray<ExoPlayer>()
>>>>>>> 501051d231c99e5878bf388804ae80c4f5938d75
    private var currentPos = 0

    inner class VH(view: View) : RecyclerView.ViewHolder(view) {
        val playerView: PlayerView = view.findViewById(R.id.playerView)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): VH {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_video, parent, false)
        return VH(view)
    }

    override fun onBindViewHolder(holder: VH, position: Int) {
<<<<<<< HEAD
        // 绑定的时候只挂载界面，不操作播放器
        holder.playerView.player = sharedPlayer
        holder.playerView.setKeepContentOnPlayerReset(true)
        holder.playerView.setShutterBackgroundColor(android.graphics.Color.DKGRAY)
=======
        val uri = videos[position]
        var player = playerPool.get(position)

        if (player == null) {
            val renderersFactory = DefaultRenderersFactory(context)
                .setEnableDecoderFallback(true)

            player = ExoPlayer.Builder(context, renderersFactory).build()
            player.setMediaItem(MediaItem.fromUri(uri))
            player.repeatMode = Player.REPEAT_MODE_ONE
            
            val saved = historyStore.getPosition(uri.toString())
            if (saved > 0) player.seekTo(saved)
            
            player.volume = 0f
            player.prepare()
            
            // 强制预渲染
            player.playWhenReady = true
            player.pause()
            
            playerPool.put(position, player)
        }

        // 【绝杀1】彻底防止画框重建时黑屏：保留最后一帧残影
        holder.playerView.setKeepContentOnPlayerReset(true)
        // 【绝杀2】设置一个深灰色背景，哪怕万一没画面，也不是死黑
        holder.playerView.setShutterBackgroundColor(android.graphics.Color.DKGRAY)
        
        holder.playerView.player = player

        if (position == currentPos) {
            player.volume = 1f
            player.play()
        } else {
            player.volume = 0f
            player.pause()
        }
>>>>>>> 501051d231c99e5878bf388804ae80c4f5938d75

        holder.itemView.setOnClickListener {
            sharedPlayer?.let { p ->
                if (p.isPlaying) p.pause() else p.play()
            }
        }

        holder.itemView.setOnLongClickListener {
            onLongPress()
            true
        }
    }

    override fun onViewRecycled(holder: VH) {
        super.onViewRecycled(holder)
<<<<<<< HEAD
        // 不要清空 player，保留残影，防止黑屏！
=======
        // 【修改】不要直接清空 player，让画面残留在上面。
        // 直到新的视频绑定上来，才会覆盖掉。这样就绝对不会闪黑！
>>>>>>> 501051d231c99e5878bf388804ae80c4f5938d75
    }

    override fun getItemCount() = videos.size

    // 当页面切换时，由 MainActivity 触发
    fun setCurrent(position: Int) {
<<<<<<< HEAD
        if (position == currentPos && sharedPlayer != null) return
        currentPos = position

        // 初始化唯一的播放器
        if (sharedPlayer == null) {
            val renderersFactory = DefaultRenderersFactory(context).setEnableDecoderFallback(true)
            sharedPlayer = ExoPlayer.Builder(context, renderersFactory).build()
            sharedPlayer?.repeatMode = Player.REPEAT_MODE_ONE
        }

        val uri = videos[position]
        // 保存上一个视频的进度
        historyStore.savePosition(uri.toString(), sharedPlayer?.currentPosition ?: 0L)

        // 换台！
        sharedPlayer?.let { player ->
            player.setMediaItem(MediaItem.fromUri(uri))
            val saved = historyStore.getPosition(uri.toString())
            if (saved > 0) player.seekTo(saved)
            player.prepare()
            player.play()
=======
        playerPool.get(currentPos)?.let {
            historyStore.savePosition(videos[currentPos].toString(), it.currentPosition)
            it.pause()
            it.volume = 0f
        }

        currentPos = position

        playerPool.get(position)?.let {
            it.volume = 1f
            it.play()
>>>>>>> 501051d231c99e5878bf388804ae80c4f5938d75
        }

        val keysToRemove = mutableListOf<Int>()
        for (i in 0 until playerPool.size()) {
            val key = playerPool.keyAt(i)
            if (abs(key - currentPos) > 3) {
                val p = playerPool.valueAt(i)
                historyStore.savePosition(videos[key].toString(), p.currentPosition)
                p.release()
                keysToRemove.add(key)
            }
        }
        keysToRemove.forEach { playerPool.remove(it) }
    }

    fun saveCurrentPosition() {
<<<<<<< HEAD
        sharedPlayer?.let {
=======
        playerPool.get(currentPos)?.let {
>>>>>>> 501051d231c99e5878bf388804ae80c4f5938d75
            historyStore.savePosition(videos[currentPos].toString(), it.currentPosition)
        }
    }

    fun releaseAll() {
<<<<<<< HEAD
        sharedPlayer?.release()
        sharedPlayer = null
=======
        for (i in 0 until playerPool.size()) {
            val p = playerPool.valueAt(i)
            historyStore.savePosition(videos[playerPool.keyAt(i)].toString(), p.currentPosition)
            p.release()
        }
        playerPool.clear()
>>>>>>> 501051d231c99e5878bf388804ae80c4f5938d75
    }
}
