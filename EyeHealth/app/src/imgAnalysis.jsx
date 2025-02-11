import React, { useState } from "react";

const PatientImages = () => {
  const [images, setImages] = useState([
    {
      id: 1,
      patientName: "Иван Иванов",
      cardNumber: "123456",
      imageUrl: "https://via.placeholder.com/150",
      analysisResult: "Здоров",
    },
    {
      id: 2,
      patientName: "Мария Петрова",
      cardNumber: "654321",
      imageUrl: "https://via.placeholder.com/150",
      analysisResult: "Необходимо дополнительное обследование",
    },
  ]);

  const handleDelete = (id) => {
    setImages(images.filter(image => image.id !== id));
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl font-bold mb-4 text-center">Загруженные снимки</h2>

        {images.length === 0 ? (
          <p className="text-center text-gray-700">Нет загруженных снимков.</p>
        ) : (
          images.map((image) => (
            <div key={image.id} className="mb-6">
              <div className="flex items-center mb-3">
                <img
                  src={image.imageUrl}
                  alt="Снимок пациента"
                  className="w-20 h-20 object-cover mr-4"
                />
                <div>
                  <p className="font-semibold text-gray-900">{image.patientName}</p>
                  <p className="text-gray-700">Номер карты: {image.cardNumber}</p>
                </div>
              </div>

              <p className="text-gray-700 mb-2">Результат анализа: {image.analysisResult}</p>

              <button
                onClick={() => handleDelete(image.id)}
                className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition"
              >
                Удалить снимок
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default PatientImages;
