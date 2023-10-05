import { useState } from "react";
import Button, { ButtonProps } from "./Button";
import _ from "lodash";
import CustomDialog from "./CustomDialog";
import { isPropertySignature } from "typescript";

export interface ModalRenderProps {
  handleClose: () => void;
  handleOpen: () => void;
}

export interface ModalProps extends ButtonProps {
  title: string;
  render: React.ComponentType<ModalRenderProps>;
  width?: "md" | "lg" | "xl";
}

export default function Modal({
  render: RenderComponent,
  ...props
}: ModalProps) {
  const [open, setOpen] = useState(false);
  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => {
    setOpen(true);
  };
  return (
    <>
      <Button
        type="button"
        filled
        onClick={handleOpen}
        {..._.omit(props, "render", "title", "width")}
      >
        {props.children}
      </Button>
      <CustomDialog
        open={open}
        onClose={handleClose}
        title={props.title}
        width={props.width}
      >
        <RenderComponent handleClose={handleClose} handleOpen={handleOpen} />
      </CustomDialog>
    </>
  );
}
