import React, { FC } from "react";
import { useForm, Controller, SubmitHandler } from "react-hook-form";
import Modal, { ModalProps } from "../ui/Modal";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createAlias } from "@/api/api";
import Button from "../ui/Button";
import { AliasFormValues } from "@/types/Alias";
import { enqueueSnackbar } from "notistack";

interface ModalRenderProps {
  handleClose: () => void;
  queryClient: any;
}

export const AliasModalRender: FC<ModalRenderProps> = ({
  handleClose,
  queryClient,
}) => {
  const { handleSubmit, register } = useForm<AliasFormValues>();
  const aliasMutation = useMutation(createAlias, {
    onSuccess: () => {
      handleClose();
      queryClient.invalidateQueries("aliases");
    },
    onError: (error: any) => {
      if (
        error.response.data.detail === "You cannot have more than 10 aliases."
      ) {
        enqueueSnackbar("No puedes tener mas de 10 aliases", {
          variant: "error",
          autoHideDuration: 3000,
        });
      } else {
        enqueueSnackbar("Error en la creación de alias", {
          variant: "error",
          autoHideDuration: 3000,
        });
      }
    },
  });

  const onSubmit: SubmitHandler<AliasFormValues> = (data) => {
    aliasMutation.mutate({
      description: data?.description,
      active: data?.active,
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label
        htmlFor="description"
        className="block mt-4 text-sm font-medium text-gray-700"
      >
        Descripción
      </label>
      <textarea
        {...register("description")}
        name="description"
        id="description"
        className="mt-1 p-2 block w-full border rounded-md"
      />

      <div className="mt-6 flex justify-between">
        <Button type="button" onClick={handleClose}>
          Cancelar
        </Button>
        <Button filled type="submit">
          Crear Nuevo Correo
        </Button>
      </div>
    </form>
  );
};

interface AliasModalProps extends Partial<ModalProps> {
  queryClient: any;
}

const AliasModal: FC<AliasModalProps> = ({ queryClient, ...props }) => {
  return (
    <Modal
      title="Crear Nuevo Correo Temporal"
      render={(renderProps: any) => (
        <AliasModalRender {...renderProps} queryClient={queryClient} />
      )}
      {...props}
    >
      Nuevo Correo
    </Modal>
  );
};

export default AliasModal;
