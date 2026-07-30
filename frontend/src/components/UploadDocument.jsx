import { useRef } from "react";
import api from "../services/api";

function UploadDocument({ onUpload }) {
  const fileInputRef = useRef(null);

  const uploadFile = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post(
        "/documents/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert("Upload Successful");

      if (onUpload) {
        onUpload(response.data.filename);
      }

    } catch (error) {
      console.error(error);
      alert("Upload Failed");
    }
  };

  return (
    <>
      <button onClick={() => fileInputRef.current.click()}>
        Upload PDF
      </button>

      <input
        type="file"
        accept=".pdf"
        ref={fileInputRef}
        onChange={uploadFile}
        hidden
      />
    </>
  );
}

export default UploadDocument;