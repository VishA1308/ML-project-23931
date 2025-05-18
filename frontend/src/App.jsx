import { useState } from 'react'
import appLogo from './assets/app_icon.svg'
import './App.css'
import { Editor } from './Editor';

function App() {
  const [preview, setPreview] = useState(null);
  const [fileType, setFileType] = useState('image'); // 'image' or 'pdf'
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');
  const [result, setResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setSelectedFile(file);

    if (fileType === 'image') {
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(file);
    } else {
      setPreview(URL.createObjectURL(file));
    }

    console.log("Selected file:", file);
  };

  const mockTextRecognition = async (file) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          text: "Образец №: 4171014164\n" +
              "Вид материала: Венозная кровь\n" +
              "\n" +
              "Регистрация: 15.01.2025 07:37:57 *\n" +
              "\n" +
              "Витамин D, 25-гидрокси (кальциферол)\n" +
              "\n" +
              "Метод и оборудование: Иммунохемилюминесцентный анализ (UniCel DxI 800, Beckman Coulter, США)\n" +
              "\n" +
              "Название/показатель Результат Референные значения **\n" +
              "Концентрация 34.82 нг/мл 30.00 - 100.00\n" +
              "\n" +
              "Комментарий: <20 нг/мл - дефицит; 20-30 нг/мл - недостаточность; 30-100 нг/мл - оптимальный уровень."
        });
      }, 1500);
    });
  };

  const processFile = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      // const response = await fetch('YOUR_API_ENDPOINT', {
      //   method: 'POST',
      //   body: formData,
      //   // headers: { 'Authorization': 'Bearer YOUR_TOKEN' } // if needed
      // });

      // if (!response.ok) throw new Error('API request failed');

      // const data = await response.json();
      const data = await mockTextRecognition(formData);
      setResult(data.text); // Assuming API returns { text: "..." }
    } catch (err) {
      setError(err.message);
      console.error('Processing error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <div className="app-header">
        <a href="https://github.com/VishA1308/ML-project-23931" target="_blank" rel="noreferrer">
          <img src={appLogo} className="logo" alt="App logo" />
        </a>
        <h1>Распознавание результатов анализов</h1>
      </div>


      <div className="file-upload-container">
        {/* File type selector */}
        <div className="file-type-selector">
          <button
            className={`selector-btn ${fileType === 'image' ? 'active' : ''}`}
            onClick={() => {
              setFileType('image');
              setPreview(null);
            }}
          >
            <svg className="selector-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Изображение
          </button>
          <button
            className={`selector-btn ${fileType === 'pdf' ? 'active' : ''}`}
            onClick={() => {
              setFileType('pdf');
              setPreview(null);
            }}
          >
            <svg className="selector-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            PDF
          </button>
        </div>

        {/* File input */}
        <input
          type="file"
          id="fileUpload"
          accept={fileType === 'image' ? 'image/*' : 'application/pdf'}
          onChange={handleFileUpload}
          className="hidden-input"
        />

        {/* Upload button */}
        <label htmlFor="fileUpload" className="upload-button">
          <svg className="upload-icon" /* ... your SVG ... */ />
          Загрузить {fileType === 'image' ? 'Изображение' : 'PDF'}
        </label>

        {preview && (
            <div className="preview-action-container">
              <div className="preview-container">
                {fileType === 'image' ? (
                    <img src={preview} alt="Preview" className="preview-content" />
                ) : (
                    <iframe
                        src={preview}
                        className="preview-content pdf-preview"
                        title="PDF Preview"
                    />
                )}
              </div>

              {/* Status */}
              <div className="file-status">
                {preview ? `${fileType.toUpperCase()} loaded` : 'No file selected'}
              </div>

              <button
                  className={`process-button ${isLoading ? 'loading' : ''}`}
                  onClick={processFile}
                  disabled={isLoading}
              >
                {isLoading ? 'Обработка...' : 'Распознать текст'}
              </button>

            <div className="result-container">
              <div className="result-header">
                <h3>Результат распознавания:</h3>
                <div className="result-controls">
                  <button
                      className="edit-toggle"
                      onClick={() => setIsEditing(!isEditing)}
                  >
                    {isEditing ? 'Заблокировать' : 'Редактировать'}
                  </button>
                  <button
                      className="copy-button"
                      onClick={() => navigator.clipboard.writeText(result)}
                  >
                    Копировать
                  </button>
                </div>
              </div>
              <Editor
                  initialValue={result}
                  editable={isEditing}
                  onChange={(newText) => setResult(newText)}
              />
            </div>
            </div>
        )}
      </div>


      <p className="app info">
        v1.0
      </p>
    </>
  )
}

export default App
