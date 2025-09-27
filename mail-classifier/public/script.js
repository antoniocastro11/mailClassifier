const form = document.getElementById("emailForm");
const loading = document.getElementById("loading");
const resultDiv = document.getElementById("result");
const categorySpan = document.getElementById("category");
const responseText = document.getElementById("responseText");
const errorMsg = document.getElementById("errorMsg");

const emailTextArea = document.getElementById("emailText");
const fileInput = document.getElementById("fileUpload");

const clearTextBtn = document.getElementById("clearBtn");
const clearFileBtn = document.getElementById("clearFileBtn");

clearTextBtn.addEventListener("click", () => {
  emailTextArea.value = "";
  errorMsg.classList.add("hidden");
  resultDiv.classList.add("hidden");
});

clearFileBtn.addEventListener("click", () => {
  fileInput.value = "";
  errorMsg.classList.add("hidden");
  resultDiv.classList.add("hidden");
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorMsg.classList.add("hidden");
  resultDiv.classList.add("hidden");

  const emailText = emailTextArea.value.trim();
  const hasFile = fileInput.files.length > 0;

  try {
    if (emailText && hasFile) {
      throw new Error("Envie apenas texto ou apenas arquivo, não ambos.");
    }

    if (!emailText && !hasFile) {
      throw new Error("Por favor, insira o texto do email ou envie um arquivo.");
    }

    if (hasFile) {
      const file = fileInput.files[0];
      const allowedTypes = ["text/plain", "application/pdf"];

      if (!allowedTypes.includes(file.type)) {
        throw new Error("Formato inválido! Apenas .txt ou .pdf são permitidos.");
      }

      if (file.size > 2 * 1024 * 1024) {
        throw new Error("Arquivo muito grande! Máximo permitido é 2MB.");
      }
    }

    loading.classList.remove("hidden");

    const payload = new FormData();
    if (emailText) payload.append("email", emailText);
    if (hasFile) payload.append("file", fileInput.files[0]);

    const response = await fetch("https://mailclassifier-gilt.vercel.app/api/classify", {
      method: "POST",
      body: payload,
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || "Erro no servidor");
    }

    const data = await response.json();

    categorySpan.textContent = data.categoria;
    responseText.textContent = data.resposta;
    resultDiv.classList.remove("hidden");

  } catch (error) {
    errorMsg.textContent = error.message;
    errorMsg.classList.remove("hidden");
  } finally {
    loading.classList.add("hidden");
  }
});
