import React, { useState } from 'react'

export default function InputBox({ onSendMessage, loading }) {
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input)
      setInput('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="glass-effect card-premium border border-white/20 p-4">
      <div className="flex gap-3">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Share your thoughts... (Shift+Enter for new line)"
          disabled={loading}
          className="flex-1 bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-white/50 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300 disabled:opacity-50"
          rows="3"
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="btn-primary self-end disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <span className="inline-block animate-spin mr-2">⌛</span>
              Thinking...
            </>
          ) : (
            <>
              <span className="mr-2">→</span>
              Send
            </>
          )}
        </button>
      </div>
      <p className="text-white/40 text-xs mt-2">
        🔐 Your conversations are processed with emotional intelligence
      </p>
    </div>
  )
}
