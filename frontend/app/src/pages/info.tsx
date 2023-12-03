import Head from "next/head";
import Link from "next/link";
import Image from "next/image";
import Button from "@/components/ui/Button";

export default function Info() {
  return (
    <div className="flex h-screen flex-col items-center justify-center bg-primary p-4">
      <Head>
        <title>Información | Chinchilla Mail</title>
      </Head>
      <div className="flex flex-col items-center bg-white p-8 rounded-lg max-w-4xl shadow-md">
        <h1 className="text-3xl font-bold text-gray-800 mb-4 flex items-center">
          <Image
            src={`/icons/info.svg`}
            width={32}
            height={32}
            alt="Chinchilla Mail Logo"
            className="ml-4"
          />
          Acerca de Chinchilla Mail
        </h1>
        <p className="text-lg text-gray-600 mb-4">
          Chinchilla Mail es un trabajo de memoria desarrollado por Sebastián
          Valdivia, que busca proporcionar una solución de proxy de correos
          temporales para mejorar la seguridad y privacidad de los usuarios en
          línea. Este sistema permite a los usuarios manejar y recibir correos
          electrónicos sin exponer su dirección de correo real.
        </p>
        <p className="text-lg text-gray-600 mb-4">
          Este sistema comunitario de código abierto y gratuito se ha diseñado
          con el objetivo de ser una herramienta útil para la realización de
          futuros estudios sobre la privacidad del correo electrónico en Chile.
        </p>
        <Link href="/" className="text-blue-700 hover:text-blue-900 mt-4">
          Volver a Inicio
        </Link>
      </div>
    </div>
  );
}
