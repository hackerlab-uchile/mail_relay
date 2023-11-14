import React, { FC, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import Modal, { ModalProps } from "../ui/Modal";
import Button from "../ui/Button";
import { useMutation } from "@tanstack/react-query";
import { deleteAlias } from "@/api/api";

interface ModalRenderProps {
  handleClose: () => void;
  aliasId: number;
  aliasName: string;
  queryClient: any;
}

interface DeleteAliasFormValues {
  confirmAliasName: string;
}

export const DeleteAliasModalRender: FC<ModalRenderProps> = ({
  aliasId,
  aliasName,
  queryClient,
  handleClose,
}) => {
  const { handleSubmit, register, watch, reset } =
    useForm<DeleteAliasFormValues>();
  const confirmAliasName = watch("confirmAliasName");
  const aliasNameBeforeAt = aliasName.split("@")[0];
  const isConfirmed = confirmAliasName === aliasNameBeforeAt;

  const deleteMutation = useMutation(() => deleteAlias(aliasId), {
    onSuccess: () => {
      handleClose();
      queryClient.invalidateQueries(["aliases"]);
      reset();
    },
  });

  const onSubmit: SubmitHandler<DeleteAliasFormValues> = () => {
    if (isConfirmed) {
      deleteMutation.mutate();
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <p>
        Porfavor escriba <strong>{aliasNameBeforeAt}</strong> para confirmar.
      </p>
      <input
        {...register("confirmAliasName", { required: true })}
        type="text"
        className="mt-1 p-2 block w-full border rounded-md"
      />
      <div className="mt-6 flex justify-between">
        <Button type="button" onClick={handleClose}>
          Cancelar
        </Button>
        <Button
          filled
          className="bg-red-500 border-red-500"
          type="submit"
          disabled={!isConfirmed}
        >
          Borrar
        </Button>
      </div>
    </form>
  );
};

interface DeleteAliasModalProps extends Partial<ModalProps> {
  queryClient: any;
  aliasId: number;
  aliasName: string;
}

const DeleteAliasModal: FC<DeleteAliasModalProps> = ({
  queryClient,
  aliasId,
  aliasName,
  ...props
}) => {
  return (
    <Modal
      className="bg-red-500 border-red-500 "
      icon="trash-solid"
      title="Confirmar Borrado de Correo"
      render={(renderProps: any) => (
        <DeleteAliasModalRender
          {...renderProps}
          queryClient={queryClient}
          aliasName={aliasName}
          aliasId={aliasId}
        />
      )}
      {...props}
    />
  );
};

export default DeleteAliasModal;
