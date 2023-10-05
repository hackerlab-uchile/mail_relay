import Toggle from "@/components/ui/Toggle";
import { useState } from "react";

export default function IndexPage() {
  const [aliases, setAliases] = useState([
    { name: "alias1", active: true },
    { name: "alias2", active: false },
  ]);
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleAlias = (index: number) => {
    const newAliases = [...aliases];
    newAliases[index].active = !newAliases[index].active;
    setAliases(newAliases);
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 dark:bg-gray-900">
        <div className="max-w-screen-xl flex items-center justify-between mx-auto p-4">
          <div className="flex items-center">
            <h1 className="text-2xl font-semibold text-black dark:text-white mr-6">
              Mail Relay
            </h1>
            <input
              type="text"
              placeholder="Search aliases..."
              className="p-2 rounded border mr-6"
            />
            <button className="bg-blue-500 text-white p-2 rounded">
              New Alias
            </button>
          </div>
          <div className="flex items-center">
            <button
              type="button"
              className="flex mr-3 text-sm bg-gray-800 rounded-full md:mr-0 focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
              id="user-menu-button"
              aria-expanded="false"
              onClick={() => setMenuOpen(!menuOpen)}
            >
              <img
                className="w-8 h-8 rounded-full"
                src="/docs/images/people/profile-picture-3.jpg"
                alt="user photo"
              />
            </button>
            {/* Dropdown menu */}
            {menuOpen && (
              <div className="z-50 absolute right-0 mt-2 text-base list-none bg-white divide-y divide-gray-100 rounded-lg shadow dark:bg-gray-700 dark:divide-gray-600">
                <div className="px-4 py-3">
                  <span className="block text-sm text-gray-900 dark:text-white">
                    Username
                  </span>
                </div>
                <ul aria-labelledby="user-menu-button">
                  <li>
                    <a
                      href="#"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white"
                    >
                      Dashboard
                    </a>
                  </li>
                  <li>
                    <a
                      href="#"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white"
                    >
                      Settings
                    </a>
                  </li>
                  <li>
                    <a
                      href="#"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white"
                    >
                      Logout
                    </a>
                  </li>
                </ul>
              </div>
            )}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="p-8">
        <table className="min-w-full bg-white rounded-lg overflow-hidden">
          <thead>
            <tr>
              <th className="px-6 py-4 text-left">Alias Name</th>
              <th className="px-6 py-4 text-left">Active</th>
            </tr>
          </thead>
          <tbody>
            {aliases.map((alias, index) => (
              <tr key={index} className="hover:bg-gray-100">
                <td className="px-6 py-4">{alias.name}</td>
                <td className="px-6 py-4">
                  <Toggle
                    isActive={alias.active}
                    onToggle={() => toggleAlias(index)}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}
