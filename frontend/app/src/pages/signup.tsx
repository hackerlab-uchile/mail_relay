import Head from "next/head";
import { useRouter } from "next/router";
import { SubmitHandler, useForm } from "react-hook-form";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { signupUser } from "@/api/api";
import { SnackbarProvider, enqueueSnackbar, useSnackbar } from "notistack";
import Script from "next/script";
import { UsuarioCreate } from "@/types/Usuario";
import Link from "next/link";
import Image from "next/image";

type SignupInputs = {
  username: string;
  recipient_email: string;
  password: string;
  turnstileToken?: string;
};

let CLOUDFLARE_SITE_KEY = process.env.NEXT_PUBLIC_CLOUDFLARE_SITE_KEY;

export default function Signup() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { register, handleSubmit, setValue } = useForm<SignupInputs>();
  const { enqueueSnackbar } = useSnackbar();

  const signupMutation = useMutation(signupUser, {
    onSuccess: () => {
      router.push("/login");
      enqueueSnackbar("La cuenta se creó correctamente", {
        variant: "success",
        preventDuplicate: true,
        autoHideDuration: 3000,
      });
    },
    onError: (error: any) => {
      enqueueSnackbar("Error en la creación de cuenta", {
        variant: "error",
        autoHideDuration: 3000,
      });
    },
  });

  const onSubmit: SubmitHandler<SignupInputs> = async (data, event) => {
    // Prevent the default form submission
    event?.preventDefault();

    // Retrieve the Turnstile token from the form
    const token = event?.target["cf-turnstile-response"]?.value;

    if (token) {
      // Construct the user object expected by the backend
      const user: UsuarioCreate = {
        username: data.username,
        recipient_email: data.recipient_email,
        password: data.password,
        turnstile_response: token,
      };

      // Send the user object and the Turnstile response token to the server
      signupMutation.mutate(user);
    } else {
      // Handle the error case where the token is missing
      enqueueSnackbar("Complete el Captcha correctamente", {
        variant: "error",
        autoHideDuration: 3000,
      });
    }
  };

  return (
    <div className="flex h-screen flex-col items-center justify-start bg-primary">
      <Head>
        <title>Registrarse | Chinchilla Mail</title>
      </Head>
      <Script
        src="https://challenges.cloudflare.com/turnstile/v0/api.js"
        async
        defer
      ></Script>
      <div className="flex items-center">
        <h1
          className="text-6xl font-extrabold text-white "
          style={{ WebkitTextStroke: "2px black" }}
        >
          Chinchilla Mail
        </h1>
        <Image
          src={`/icons/logo.svg`}
          width={128}
          height={128}
          alt="Chinchilla Mail Logo"
          className="ml-4"
        />
      </div>
      <form
        className="z-10 rounded-lg bg-white p-10 shadow-md"
        onSubmit={handleSubmit(onSubmit)}
      >
        <h2 className="mb-8 text-center text-2xl font-bold text-gray-800">
          Crear Cuenta
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
        <div className="mb-4">
          <label
            className="mb-2 block font-bold text-gray-700"
            htmlFor="recipient_email"
          >
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
        <div
          className="cf-turnstile mb-6"
          data-sitekey={CLOUDFLARE_SITE_KEY}
          data-callback="javascriptCallback"
        ></div>
        <button
          className="w-full rounded-lg bg-blue-500 py-2 px-4 font-bold text-white hover:bg-blue-700"
          type="submit"
        >
          Registrar
        </button>
        <div className="mt-4 text-center">
          <p>
            ¿Ya tienes cuenta?{" "}
            <Link className="text-blue-700" href="/login">
              Vuelve al inicio de sesión
            </Link>
          </p>
        </div>
      </form>
    </div>
  );
}
