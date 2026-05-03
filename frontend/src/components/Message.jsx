import React, { useState } from 'react'

const emotionColors = {
  'Angry': { bg: 'bg-red-500/20', border: 'border-red-500/40', text: 'text-red-100', badge: 'bg-red-500/30' },
  'Sad': { bg: 'bg-cyan-500/20', border: 'border-cyan-500/40', text: 'text-cyan-100', badge: 'bg-cyan-500/30' },
  'Happy': { bg: 'bg-green-500/20', border: 'border-green-500/40', text: 'text-green-100', badge: 'bg-green-500/30' },
  'Urgent': { bg: 'bg-orange-500/20', border: 'border-orange-500/40', text: 'text-orange-100', badge: 'bg-orange-500/30' },
  'Neutral': { bg: 'bg-gray-500/20', border: 'border-gray-500/40', text: 'text-gray-100', badge: 'bg-gray-500/30' }
}

export default function Message({ message }) {
  const [showNormal, setShowNormal] = useState(false)

  if (message.type === 'error') {
    return (
      <div className="animate-slideInLeft">
        <div className="bg-red-500/20 border border-red-500/40 rounded-lg p-4 text-red-100 text-sm">
          ⚠️ {message.content}
        </div>
      </div>
    )
  }

  if (message.type === 'user') {
    return (
      <div className="animate-slideInLeft flex justify-end">
        <div className="bg-gradient-to-r from-purple-600 to-purple-700 rounded-2xl rounded-br-none px-6 py-3 max-w-xs lg:max-w-md">
          <p className="text-white text-sm">{message.content}</p>
          <p className="text-purple-200 text-xs mt-1">
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>
      </div>
    )
  }

  if (message.type === 'bot') {
    const colors = emotionColors[message.emotion] || emotionColors['Neutral']

    return (
      <div className="animate-slideInRight">
        <div className={`${colors.bg} border ${colors.border} rounded-2xl rounded-bl-none p-4 space-y-3`}>
          {/* Emotion Badge */}
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`emotion-badge ${colors.badge} ${colors.text} text-xs`}>
              {message.emotion}
            </span>
            <span className={`text-xs ${colors.text}`}>
              {message.intensity} • {message.confidence}
            </span>
          </div>

          {/* Main Response */}
          <div className={`${colors.text} text-sm leading-relaxed whitespace-pre-wrap break-words`}>
            {message.content}
          </div>

          {/* Show Normal Response Toggle */}
          {message.normalResponse && (
            <button
              onClick={() => setShowNormal(!showNormal)}
              className={`text-xs transition-all duration-300 ${colors.text} hover:${colors.text} opacity-70 hover:opacity-100`}
            >
              {showNormal ? '🔽 Hide normal response' : '🔼 Show normal response'}
            </button>
          )}

          {/* Normal Response */}
          {showNormal && message.normalResponse && (
            <div className={`mt-3 pt-3 border-t ${colors.border} opacity-75`}>
              <p className="text-xs font-semibold mb-2">Standard AI Response:</p>
              <div className={`${colors.text} text-xs whitespace-pre-wrap break-words`}>
                {message.normalResponse}
              </div>
            </div>
          )}

          {/* Timestamp */}
          <p className={`text-xs ${colors.text} opacity-60`}>
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>
      </div>
    )
  }
}
