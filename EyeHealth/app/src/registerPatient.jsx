import { useState } from "react";

export default function PatientsPage() {
  const [search, setSearch] = useState("");
  const patients = [
    { id: 1, name: "Иванов Иван", email: "ivanov2004@gmail.com", card: "10453", phone: "2453546", address: "Минск" },
    { id: 2, name: "Иванов Иван", email: "ivanov2004@gmail.com", card: "10453", phone: "2453546", address: "Минск" },
    { id: 3, name: "Иванов Иван", email: "ivanov2004@gmail.com", card: "10453", phone: "2453546", address: "Минск" },
  ];

  return (
    <div className="flex min-h-screen">
      <aside className="w-64 bg-gray-100 p-6">
        <h2 className="text-xl font-semibold">Eye Health Assistant</h2>
        <nav className="mt-6">
          <ul>
            <li className="py-2 text-purple-700 font-bold">Личный кабинет</li>
            <li className="py-2">Загрузка фото</li>
            <li className="py-2">Пациенты</li>
          </ul>
        </nav>
      </aside>
      <main className="flex-1 p-6">
        <h1 className="text-2xl font-bold text-purple-700">Пациенты</h1>
        <p className="text-gray-600">Добро пожаловать, с возвращением к работе!</p>
        <div className="flex mt-4">
          <input
            type="text"
            placeholder="Иванов..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="p-2 border rounded w-full"
          />
          <button className="bg-purple-700 text-white px-4 py-2 ml-2 rounded">ПОИСК</button>
        </div>
        <button className="bg-purple-700 text-white px-4 py-2 mt-4 rounded">ДОБАВИТЬ ПАЦИЕНТА</button>
        <table className="mt-6 w-full border-collapse border border-gray-200">
          <thead>
            <tr className="bg-gray-100">
              <th className="border p-2">✔</th>
              <th className="border p-2">ИМЯ</th>
              <th className="border p-2">НОМЕР МЕДИЦИНСКОЙ КАРТЫ</th>
              <th className="border p-2">ТЕЛЕФОН</th>
              <th className="border p-2">АДРЕС</th>
              <th className="border p-2">ДЕЙСТВИЯ</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((patient) => (
              <tr key={patient.id} className="border">
                <td className="border p-2"><input type="checkbox" /></td>
                <td className="border p-2">{patient.name}<br/><span className="text-gray-500 text-sm">{patient.email}</span></td>
                <td className="border p-2">{patient.card}</td>
                <td className="border p-2">{patient.phone}</td>
                <td className="border p-2">{patient.address}</td>
                <td className="border p-2 text-blue-600 cursor-pointer">Просмотреть</td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}

export function RegisterPatient() {
  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-gray-800">Eye Health Assistant</h1>
      <div className="bg-white p-6 mt-6 rounded shadow-md w-full max-w-md">
        <h2 className="text-xl font-bold">Укажите данные пациента</h2>
        <input className="w-full p-2 border rounded mt-4" placeholder="ФИО" />
        <input className="w-full p-2 border rounded mt-4" placeholder="Пол" />
        <input className="w-full p-2 border rounded mt-4" placeholder="Дата рождения" />
        <input className="w-full p-2 border rounded mt-4" placeholder="Телефон" />
        <input className="w-full p-2 border rounded mt-4" placeholder="Адрес" />
        <input className="w-full p-2 border rounded mt-4" placeholder="Номер медицинской карты" />
        <button className="bg-purple-700 text-white px-4 py-2 mt-4 rounded w-full">Добавить пациента</button>
      </div>
    </div>
  );
}
