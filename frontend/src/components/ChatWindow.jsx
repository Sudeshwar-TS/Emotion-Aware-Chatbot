import React from 'react'
import Message from './Message'

export default function ChatWindow({ messages, messagesEndRef }) {
  return (
    <div className="flex-1 overflow-y-auto glass-effect card-premium border border-white/20 p-6 mb-4 space-y-4">
      {messages.length === 0 ? (
        <div className="h-full flex flex-col items-center justify-center text-white/50">
          <div className="text-6xl mb-4">💬</div>
          <p className="text-lg font-semibold">Start a conversation</p>
          <p className="text-sm mt-2">Share your thoughts and discover emotion-aware responses</p>
        </div>
      ) : (
        <>
          {messages.map((message, idx) => (
            <Message key={idx} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  )
}
