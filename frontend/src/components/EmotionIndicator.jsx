import React from 'react'

const emotionEmojis = {
  'Angry': '😠',
  'Sad': '😢',
  'Happy': '😊',
  'Urgent': '⚡',
  'Neutral': '😐'
}

const emotionGradients = {
  'Angry': 'from-red-500 to-red-600',
  'Sad': 'from-cyan-500 to-blue-600',
  'Happy': 'from-green-500 to-emerald-600',
  'Urgent': 'from-orange-500 to-red-600',
  'Neutral': 'from-gray-500 to-slate-600'
}

export default function EmotionIndicator({ currentEmotion }) {
  if (!currentEmotion) {
    return (
      <div className="glass-effect card-premium border border-white/20 p-6">
        <h3 className="text-white text-sm font-bold mb-4 uppercase tracking-wider">Current Emotion</h3>
        <div className="flex flex-col items-center justify-center py-8">
          <div className="text-5xl mb-3 opacity-50">🎭</div>
          <p className="text-white/50 text-sm text-center">Waiting for emotion detection...</p>
        </div>
      </div>
    )
  }

  const emoji = emotionEmojis[currentEmotion.emotion] || '😐'
  const gradient = emotionGradients[currentEmotion.emotion] || 'from-gray-500 to-slate-600'

  return (
    <div className="glass-effect card-premium border border-white/20 p-6 space-y-4">
      <h3 className="text-white text-sm font-bold uppercase tracking-wider">Current Emotion</h3>

      {/* Emotion Circle */}
      <div className={`w-full aspect-square rounded-full bg-gradient-to-br ${gradient} flex items-center justify-center shadow-2xl`}>
        <span className="text-9xl">{emoji}</span>
      </div>

      {/* Emotion Name */}
      <div className="text-center">
        <p className="text-white text-2xl font-bold">{currentEmotion.emotion}</p>
        <p className="text-white/60 text-sm">{currentEmotion.intensity} Intensity</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-white/10 rounded-lg p-3 text-center">
          <p className="text-white/60 text-xs mb-1">Confidence</p>
          <p className="text-white text-lg font-bold">{currentEmotion.confidence}</p>
        </div>
        <div className="bg-white/10 rounded-lg p-3 text-center">
          <p className="text-white/60 text-xs mb-1">Response Speed</p>
          <p className="text-white text-lg font-bold">{currentEmotion.responseSpeed}</p>
        </div>
      </div>

      {/* Color Indicator */}
      <div className="flex items-center gap-2">
        <div
          className="w-6 h-6 rounded-full shadow-lg"
          style={{
            background: {
              'RED': '#FF6B6B',
              'BLUE': '#4ECDC4',
              'GREEN': '#45B7D1',
              'ORANGE': '#FFA500',
              'GRAY': '#95A5A6'
            }[currentEmotion.uiColor] || '#95A5A6'
          }}
        ></div>
        <p className="text-white/60 text-xs">UI Color: <span className="font-semibold">{currentEmotion.uiColor}</span></p>
      </div>
    </div>
  )
}
