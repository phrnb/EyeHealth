import React, { useState } from "react";

const patientData = {
  id: "123456",
  name: "Иван Иванов",
  birthDate: "1990-05-15",
  gender: "Мужской",
  phone: "+7 (900) 123-45-67",
  address: "Москва, ул. Ленина, д.10, кв.5",
  scans: [
    { id: 1, date: "2024-02-10", imageUrl: "https://via.placeholder.com/150" },
    { id: 2, date: "2024-01-25", imageUrl: "https://via.placeholder.com/150" },
    { id: 3, date: "2023-12-15", imageUrl: "https://via.placeholder.com/150" },
  ],
};

const PatientProfile = () => {
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Профиль пациента</h1>

      {/* Основная информация */}
      <div className="bg-white shadow-md rounded-lg p-4 mb-6">
        <h2 className="text-xl font-semibold mb-2">Личная информация</h2>
        <p><strong>ФИО:</strong> {patientData.name}</p>
        <p><strong>Дата рождения:</strong> {patientData.birthDate}</p>
        <p><strong>Пол:</strong> {patientData.gender}</p>
        <p><strong>Телефон:</strong> {patientData.phone}</p>
        <p><strong>Адрес:</strong> {patientData.address}</p>
      </div>

      {/* Снимки пациента */}
      <div className="bg-white shadow-md rounded-lg p-4">
        <h2 className="text-xl font-semibold mb-2">Снимки пациента</h2>
        {patientData.scans.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {patientData.scans.map((scan) => (
              <div key={scan.id} className="border rounded-lg p-2 shadow-md">
                <img src={scan.imageUrl} alt={`Снимок ${scan.id}`} className="w-full rounded" />
                <p className="text-center text-sm mt-2"><strong>Дата:</strong> {scan.date}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center">Нет загруженных снимков</p>
        )}
      </div>
    </div>
  );
};

export default PatientProfile;
