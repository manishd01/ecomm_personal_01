const API_HOST = process.env.REACT_APP_API_HOST;

const AI_API = `${API_HOST}:8007`;

export const askAI = async (question, onChunk) => {
  console.log("🔥 AI API URL:", `${AI_API}/api/ai/ask`);
  console.log("🔥 Question:", question);

  try {
    const response = await fetch(`${AI_API}/api/ai/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let answer = "";

    while (true) {
      const { value, done } = await reader.read();

      if (done) break;

      const chunk = decoder.decode(value, { stream: true });

      answer += chunk;

      // update AI message here
      // setAnswer(answer);

      if (onChunk) {
        onChunk(answer);
      }
    }

    // Flush any remaining decoder content
    answer += decoder.decode();

    if (onChunk) {
      onChunk(answer);
    }

    console.log("🔥 AI Response status:", response.status);
    console.log("🔥 AI Response OK:", response.ok);

    // const responseText = await response.text();

    // console.log("🔥 AI Raw Response:", responseText);

    if (!response.ok) {
      throw new Error(`AI service failed: ${response.status}`);
    }

    // return JSON.parse(responseText);

    return answer;
  } catch (error) {
    console.error("🔥 AI SERVICE ERROR:", error);
    throw error;
  }
};

// const API_HOST = process.env.REACT_APP_API_HOST;

// const AI_API = `${API_HOST}:8007`;

// export const askAI = async (question) => {
//   const response = await fetch(`${AI_API}/api/ai/ask`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({
//       question,
//     }),
//   });

//   if (!response.ok) {
//     throw new Error("AI service request failed");
//   }

//   return response.json();
// };
