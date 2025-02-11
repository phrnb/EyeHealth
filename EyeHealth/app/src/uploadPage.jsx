import React, { useState } from "react";

const patientsData = [
  { id: "123456", name: "Иван Иванов", lastScan: "2024-02-10" },
  { id: "654321", name: "Мария Смирнова", lastScan: "2024-02-08" },
  { id: "789012", name: "Алексей Петров", lastScan: "2024-01-25" },
  { id: "345678", name: "Елена Кузнецова", lastScan: "2024-02-02" },
];

const UploadPage = () => {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredPatients = patientsData.filter((patient) =>
    patient.id.includes(searchTerm)
  );

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Загрузка снимков</h1>

      {/* Поле поиска */}
      <input
        type="text"
        placeholder="Введите номер карты..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="p-2 border rounded w-full mb-4"
      />

      {/* Таблица пациентов */}
      <div className="bg-white shadow-md rounded-lg p-4">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-200">
              <th className="p-2 text-left">Номер карты</th>
              <th className="p-2 text-left">ФИО</th>
              <th className="p-2 text-left">Дата последнего снимка</th>
              <th className="p-2 text-left">Действие</th>
            </tr>
          </thead>
          <tbody>
            {filteredPatients.length > 0 ? (
              filteredPatients.map((patient) => (
                <tr key={patient.id} className="border-b">
                  <td className="p-2">{patient.id}</td>
                  <td className="p-2">{patient.name}</td>
                  <td className="p-2">{patient.lastScan}</td>
                  <td className="p-2">
                    <button className="bg-blue-500 text-white px-4 py-1 rounded">
                      Загрузить снимок
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="p-4 text-center text-gray-500">
                  Пациент не найден
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default UploadPage;
