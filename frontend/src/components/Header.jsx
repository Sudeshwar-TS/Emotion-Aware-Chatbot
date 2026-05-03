import React from 'react'

export default function Header({ onReset }) {
  return (
    <div className="glass-effect card-premium border-b border-white/20 p-4 flex justify-between items-center">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center">
          <span className="text-xl">🤖</span>
        </div>
        <div>
          <h1 className="text-white text-xl font-bold">Emotion AI</h1>
          <p className="text-purple-200 text-xs">Premium Emotional Intelligence</p>
        </div>
      </div>

      <button
        onClick={onReset}
        className="px-4 py-2 rounded-lg text-white text-sm font-semibold bg-white/10 hover:bg-white/20 transition-all duration-300 border border-white/20 hover:border-white/40"
      >
        Clear Chat
      </button>
    </div>
  )
}
