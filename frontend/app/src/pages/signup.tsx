import Head from "next/head";
import { useRouter } from "next/router";
import { SubmitHandler, useForm } from "react-hook-form";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { signupUser } from "@/api/api";

type SignupInputs = {
  username: string;
  recipient_email: string;
  password: string;
};

export default function Signup() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { register, handleSubmit } = useForm<SignupInputs>();

  const signupMutation = useMutation(signupUser, {
    onSuccess: () => {
      router.push("/login");
    },
  });

  const onSubmit: SubmitHandler<SignupInputs> = async (data) => {
    signupMutation.mutate(data);
  };

  return (
    <div className="flex h-screen flex-col items-center justify-center bg-primary">
      <Head>
        <title>Registrarse | Mail Relay</title>
      </Head>
      <form
        className="z-10 rounded-lg bg-white p-10 shadow-md"
        onSubmit={handleSubmit(onSubmit)}
      >
        <h2 className="mb-8 text-center text-2xl font-bold text-gray-800">
          Crear Cuenta
        </h2>
        <div className="mb-4">
          <label className="mb-2 block font-bold text-gray-700" htmlFor="username">
            Usuario
          </label>
          <input
            className="w-full rounded-lg border border-gray-400 p-2"
            {...register("username", { required: true })}
          />
        </div>
        <div className="mb-4">
          <label className="mb-2 block font-bold text-gray-700" htmlFor="recipient_email">
            Email
          </label>
          <input
            className="w-full rounded-lg border border-gray-400 p-2"
            {...register("recipient_email", { required: true })}
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
          Registrar
        </button>
      </form>
    </div>
  );
}
