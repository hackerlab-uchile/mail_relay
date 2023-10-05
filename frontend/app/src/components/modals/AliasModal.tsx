import React, { FC } from "react";
import { useForm, Controller, SubmitHandler } from "react-hook-form";
import Modal, { ModalProps } from "../ui/Modal";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createAlias } from "@/api/api";
import Button from "../ui/Button";
import { AliasFormValues } from "@/types/Alias";

interface ModalRenderProps {
  handleClose: () => void;
  queryClient: any;
}

export const AliasModalRender: FC<ModalRenderProps> = ({
  handleClose,
  queryClient,
}) => {
  const { handleSubmit, control, register } = useForm<AliasFormValues>();
  const aliasMutation = useMutation(createAlias, {
    onSuccess: () => {
      handleClose();
      queryClient.invalidateQueries("aliases");
    },
  });
  const onSubmit: SubmitHandler<AliasFormValues> = (data) => {
    aliasMutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label
        htmlFor="email"
        className="block text-sm font-medium text-gray-700"
      >
        Email
      </label>
      <input
        {...register("email", { required: true })}
        type="email"
        name="email"
        id="email"
        className="mt-1 p-2 block w-full border rounded-md"
        required
      />

      <label
        htmlFor="active"
        className="block mt-4 text-sm font-medium text-gray-700"
      >
        Active
      </label>

      <label
        htmlFor="comment"
        className="block mt-4 text-sm font-medium text-gray-700"
      >
        Comentario
      </label>
      <textarea
        {...register("comment")}
        name="comment"
        id="comment"
        className="mt-1 p-2 block w-full border rounded-md"
      ></textarea>

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
