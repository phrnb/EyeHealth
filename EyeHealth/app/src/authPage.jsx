import { useState } from "react";

export default function LoginPage() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Logging in with:", { login, password, remember });
  };

  return (
    <div className="flex flex-col min-h-screen">
      <header className="bg-gray-100 py-4 px-8 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <span className="text-green-700 text-3xl">👁️</span>
          <h1 className="text-2xl font-semibold">Eye Health Assistant</h1>
        </div>
        <button className="bg-green-700 text-white px-4 py-2 rounded">Регистрация</button>
      </header>
      <main className="flex flex-1 justify-center items-center">
        <div className="bg-white p-8 rounded shadow-md w-96">
          <h2 className="text-2xl font-semibold text-center">Вход</h2>
          <p className="text-center text-gray-600">Войдите и приступайте к работе!</p>
          <form className="mt-4" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Логин"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              className="w-full p-2 border rounded mb-3"
            />
            <input
              type="password"
              placeholder="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border rounded mb-3"
            />
            <div className="flex items-center mb-3">
              <input
                type="checkbox"
                checked={remember}
                onChange={(e) => setRemember(e.target.checked)}
                className="mr-2"
              />
              <label>Сохранить данные входа</label>
            </div>
            <a href="#" className="text-blue-600 text-sm block mb-3">Забыли пароль?</a>
            <button type="submit" className="w-full bg-green-700 text-white p-2 rounded">
              Войти
            </button>
          </form>
        </div>
      </main>
      <footer className="bg-gray-800 text-white p-6 text-center">
        <div className="grid grid-cols-2 gap-4 text-left text-sm">
          <div>
            <h3 className="font-semibold">Быстрый доступ</h3>
            <ul>
              <li>Home</li>
              <li>Management</li>
              <li>About Us</li>
              <li>Become a partner</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold">Свяжитесь с нами!</h3>
            <p>(+256) 703 840 326</p>
            <p>info@mailportal.com</p>
            <p>Kizito Tower 75 Ham Hague</p>
            <p>Mai-Ha Noi – Viet Nam</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
