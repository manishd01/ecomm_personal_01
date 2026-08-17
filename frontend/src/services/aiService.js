const API_HOST = process.env.REACT_APP_API_HOST;

const AI_API = `${API_HOST}:8007`;

export const askAI = async (question) => {
  const response = await fetch(`${AI_API}/api/ai/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
    }),
  });

  if (!response.ok) {
    throw new Error("AI service request failed");
  }

  return response.json();
};
