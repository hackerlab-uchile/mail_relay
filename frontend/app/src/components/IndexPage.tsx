import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { logout, useUser } from "@/hooks/auth";
import { getAliases, updateAlias, deleteAlias } from "@/api/api";
import { Alias } from "@/types/Alias";
import Toggle from "./ui/Toggle";
import Button from "./ui/Button";
import AliasModal from "./modals/AliasModal";
import DeleteAliasModal from "./modals/DeleteAliasModal";
import { FiClipboard } from "react-icons/fi";
import { enqueueSnackbar } from "notistack";
import Image from "next/image";
import Link from "next/link";

export default function IndexPage() {
  const [menuOpen, setMenuOpen] = useState(false);

  const queryClient = useQueryClient();
  const logoutMutation = useMutation(logout, {
    onSuccess: () => {
      queryClient.invalidateQueries(["usuario", "me"]);
    },
  });

  const handleLogout = () => {
    logoutMutation.mutate();
  };

  const aliasesQuery = useQuery<Alias[]>({
    queryKey: ["aliases"],
    queryFn: getAliases,
  });

  const toggleAliasMutation = useMutation(
    (params: { aliasId: number; updatedAlias: Partial<Alias> }) =>
      updateAlias(params.aliasId, params.updatedAlias),
    {
      onSuccess: () => {
        // Invalidate and refetch the aliases query
        queryClient.invalidateQueries(["aliases"]);
      },
    }
  );

  const toggleAlias = (alias: Alias) => {
    toggleAliasMutation.mutate({
      aliasId: alias.id,
      updatedAlias: {
        active: !alias.active,
      },
    });
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      enqueueSnackbar("Copiado al portapapeles", {
        variant: "success",
        preventDuplicate: true,
        autoHideDuration: 3000,
      });
    });
  };

  const userQuery = useUser();

  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Header */}
      <header className="p-2 text-font dark:bg-background-dark">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center">
            <Image
              src={`/icons/logo.svg`}
              width={64}
              height={64}
              alt="Chinchilla Mail Logo"
              className=""
            />
            <h1 className="text-2xl font-semibold text-black dark:text-white mr-6">
              Chinchilla Mail
            </h1>
          </div>
          <div className="relative">
            <button
              type="button"
              className="inline-flex items-center gap-x-1 text-sm font-semibold leading-6 white:text-font dark:text-white"
              aria-expanded="false"
              onClick={() => setMenuOpen(!menuOpen)}
            >
              <span>{userQuery.data?.username}:</span>
              <span> {userQuery.data?.recipient_email}</span>
              <svg
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
                  clipRule="evenodd"
                />
              </svg>
            </button>

            {menuOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-md">
                <ul>
                  {/* <li className="px-4 py-2 hover:bg-background cursor-pointer rounded-lg">
                    Opciones
                  </li> */}
                  <li
                    className="px-4 py-2 hover:bg-background cursor-pointer rounded-lg"
                    onClick={handleLogout}
                  >
                    Cerrar Sesión
                  </li>
                </ul>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="p-8">
        <div className="flex justify-between items-center mb-4">
          <input
            type="text"
            placeholder="Buscar correos..."
            className="p-2 rounded border"
          />
          <AliasModal queryClient={queryClient} />
        </div>

        <table className="min-w-full bg-white rounded-lg overflow-hidden">
          <thead>
            <tr>
              <th className="px-6 py-4 text-left">Nombre del Correo</th>
              <th className="w-2/3 py-4 text-left">Descripción</th>
              <th className="px-6 py-4 text-left">Activo</th>
              <th className="px-6 py-4 text-left">Eliminar</th>
            </tr>
          </thead>
          <tbody>
            {aliasesQuery.data
              ?.sort((a, b) => a.id - b.id)
              .map((alias, index) => (
                <tr key={index} className="hover:bg-background">
                  <td className="px-6 py-4 flex">
                    {alias.email}
                    <FiClipboard
                      className="mt-1.5 ml-2 cursor-pointer"
                      onClick={() => copyToClipboard(alias.email)}
                    />
                  </td>
                  <td className=" py-4">{alias.description || ""}</td>
                  <td className="px-6 py-4">
                    <Toggle
                      isActive={alias.active}
                      onToggle={() => toggleAlias(alias)}
                    />
                  </td>
                  <td className="px-6 py-4">
                    <DeleteAliasModal
                      aliasId={alias.id}
                      aliasName={alias.email}
                      queryClient={queryClient}
                    />
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </main>
      <div className="absolute bottom-0 left-0 right-0 flex justify-between p-4 bg-white border-t">
        <Link
          href="/info"
          className="flex items-center text-blue-700 hover:text-blue-900"
        >
          <Image
            src={`/icons/info.svg`}
            width={24}
            height={24}
            alt="Info Icon"
            className="ml-4"
          />
          <span className="ml-2">Más información</span>
        </Link>
        <div>
          <span className="text-gray-700">
            Problemas con tu cuenta? contactanos:{" "}
          </span>
          <a
            href="mailto:contacto.chinchillamail@gmail.com"
            className="text-blue-700 hover:text-blue-900"
          >
            contacto.chinchillamail@gmail.com
          </a>
        </div>
      </div>
    </div>
  );
}
