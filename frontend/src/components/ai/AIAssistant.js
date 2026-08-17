import React, { useState } from "react";
import { askAI } from "../../services/aiService";

function AIAssistant() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim() || loading) {
      return;
    }

    const currentQuestion = question.trim();

    setMessages((previous) => [
      ...previous,
      {
        type: "user",
        text: currentQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const data = await askAI(currentQuestion);

      setMessages((previous) => [
        ...previous,
        {
          type: "assistant",
          text: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (error) {
      console.error("AI request failed:", error);

      setMessages((previous) => [
        ...previous,
        {
          type: "assistant",
          text: "Sorry, I could not connect to the AI service.",
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleAsk();
    }
  };

  return (
    <div className="ai-assistant">
      {/* Header */}
      <div className="ai-header">
        <div className="ai-header-icon">🤖</div>

        <div className="ai-header-content">
          <h1 className="ai-title">E-commerce AI Assistant</h1>

          <p className="ai-subtitle">
            Ask questions about orders, returns, refunds and company policies.
          </p>
        </div>
      </div>

      {/* Chat Area */}
      <div className="ai-chat">
        {/* Empty State */}
        {messages.length === 0 && (
          <div className="ai-empty">
            <div className="ai-empty-icon">💬</div>

            <h2 className="ai-empty-title">How can I help?</h2>

            <p className="ai-empty-description">
              Ask me anything about our e-commerce policies and services.
            </p>

            <div className="ai-suggestions">
              <button
                className="ai-suggestion-button"
                onClick={() => setQuestion("What is the refund policy?")}
              >
                What is the refund policy?
              </button>

              <button
                className="ai-suggestion-button"
                onClick={() => setQuestion("What is the return policy?")}
              >
                What is the return policy?
              </button>

              <button
                className="ai-suggestion-button"
                onClick={() => setQuestion("Can I cancel my order?")}
              >
                Can I cancel my order?
              </button>
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="ai-messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`ai-message ${
                message.type === "user"
                  ? "ai-message-user"
                  : "ai-message-assistant"
              }`}
            >
              <div className="ai-message-header">
                <div className="ai-message-avatar">
                  {message.type === "user" ? "👤" : "🤖"}
                </div>

                <strong className="ai-message-name">
                  {message.type === "user" ? "You" : "AI Assistant"}
                </strong>
              </div>

              <div className="ai-message-text">{message.text}</div>

              {/* Sources */}
              {message.type === "assistant" && message.sources?.length > 0 && (
                <div className="ai-sources">
                  <div className="ai-sources-header">
                    <span className="ai-sources-icon">📚</span>

                    <strong>Sources</strong>
                  </div>

                  <div className="ai-sources-list">
                    {message.sources.map((source, sourceIndex) => (
                      <div key={sourceIndex} className="ai-source">
                        <span className="ai-source-name">{source.source}</span>

                        <span className="ai-source-separator">—</span>

                        <span className="ai-source-chunk">
                          Chunk {source.chunk_id}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* Loading */}
          {loading && (
            <div className="ai-message ai-message-assistant">
              <div className="ai-message-header">
                <div className="ai-message-avatar">🤖</div>

                <strong className="ai-message-name">AI Assistant</strong>
              </div>

              <div className="ai-loading">
                <div className="ai-loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

                <span className="ai-loading-text">
                  Searching knowledge base and generating answer...
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="ai-input-container">
        <div className="ai-input">
          <textarea
            className="ai-input-textarea"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask something about our e-commerce platform..."
            rows={2}
            disabled={loading}
          />

          <button
            className="ai-input-button"
            onClick={handleAsk}
            disabled={loading || !question.trim()}
          >
            {loading ? (
              <>
                <span className="ai-button-spinner"></span>
                Thinking...
              </>
            ) : (
              <>
                Ask AI
                <span className="ai-button-icon">➤</span>
              </>
            )}
          </button>
        </div>

        <div className="ai-input-hint">
          Press Enter to send • Shift + Enter for a new line
        </div>
      </div>
    </div>
  );
}

export default AIAssistant;
