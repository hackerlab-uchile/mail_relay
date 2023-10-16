import Head from "next/head";
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Image from "next/image";
import Link from "next/link"; // Import Link from next/link
import { login, useUser } from "@/hooks/auth";
import { SubmitHandler, useForm } from "react-hook-form";
import { useMutation, useQueryClient } from "@tanstack/react-query";

type Inputs = {
  username: string;
  password: string;
};

export default function Home() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const loginMutation = useMutation(login, {
    onSettled: () => {
      queryClient.invalidateQueries(["usuario", "me"]);
    },
  });
  const { register, handleSubmit } = useForm<Inputs>();

  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    loginMutation.mutate(data);
  };

  const userQuery = useUser();

  useEffect(() => {
    if (!userQuery.isLoading && userQuery.isSuccess) {
      router.push("/");
    }
  }, [router, userQuery.isSuccess, userQuery.isLoading]);

  return (
    <div className="flex h-screen flex-col items-center justify-center bg-primary">
      <div className="absolute bottom-0 right-0"></div>
      <Head>
        <title>Iniciar Sesión | Mail Relay</title>
      </Head>
      <form
        className="z-10 rounded-lg bg-white p-10 shadow-md"
        onSubmit={handleSubmit(onSubmit)}
      >
        <h2 className="mb-8 text-center text-2xl font-bold text-gray-800">
          Iniciar Sesión
        </h2>
        <div className="mb-4">
          <label
            className="mb-2 block font-bold text-gray-700"
            htmlFor="username"
          >
            Usuario
          </label>
          <input
            className="w-full rounded-lg border border-gray-400 p-2"
            {...register("username", { required: true })}
          />
        </div>
        <div className="mb-6">
          <label
            className="mb-2 block font-bold text-gray-700"
            htmlFor="password"
          >
            Contraseña
          </label>
          <input
            className="w-full rounded-lg border border-gray-400 p-2"
            type="password"
            {...register("password", { required: true })}
          />
        </div>
        <button
          className="w-full rounded-lg bg-blue-500 py-2 px-4 font-bold text-white hover:bg-blue-700"
          type="submit"
        >
          Iniciar Sesión
        </button>
        <div className="mt-4 text-center">
          <p>
            ¿Aún no tienes cuenta?{" "}
            <Link className="text-blue-700" href="/signup">
              Regístrate
            </Link>
          </p>
        </div>
      </form>
    </div>
  );
}
