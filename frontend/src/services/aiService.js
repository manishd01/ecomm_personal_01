const API_HOST = process.env.REACT_APP_API_HOST;

const AI_API = `${API_HOST}:8007`;

export const askAI = async (question) => {
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

    console.log("🔥 AI Response status:", response.status);
    console.log("🔥 AI Response OK:", response.ok);

    const responseText = await response.text();

    console.log("🔥 AI Raw Response:", responseText);

    if (!response.ok) {
      throw new Error(`AI service failed: ${response.status} ${responseText}`);
    }

    return JSON.parse(responseText);
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
