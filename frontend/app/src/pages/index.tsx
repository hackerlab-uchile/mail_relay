import AuthProtected from "@/components/auth/AuthProtected";
import Head from "next/head";
import IndexPage from "@/components/IndexPage";

export default function Home() {
  return (
    <>
      <Head>
        <title>Chinchilla Mail</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <AuthProtected>
        <IndexPage />
      </AuthProtected>
    </>
  );
}
