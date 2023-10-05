import { Dialog, Transition } from "@headlessui/react";
import { Fragment } from "react";
import Button from "./Button";
import clsx from "clsx";

export default function CustomDialog(
  props: {
    open: boolean;
    onClose: () => void;
    title?: string;
    width?: "md" | "lg" | "xl";
  } & React.PropsWithChildren
) {
  const widthClassName = {
    md: "max-w-2xl",
    lg: "max-w-5xl",
    xl: "max-w-7xl",
  };
  return (
    <Transition show={props.open} as={Fragment}>
      <Dialog as="div" onClose={props.onClose} className="relative z-30">
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div
            className="fixed inset-0 bg-black bg-opacity-80"
            aria-hidden="true"
          />
        </Transition.Child>

        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0 scale-95"
          enterTo="opacity-100 scale-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100 scale-100"
          leaveTo="opacity-0 scale-95"
        >
          <div className="fixed inset-0 overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4">
              {/*<Dialog.Panel className="mx-auto max-w-sm rounded bg-white">*/}
              <Dialog.Panel
                className={clsx(
                  widthClassName[props.width || "md"],
                  "w-full transform overflow-visible rounded-2xl bg-white",
                  "py-6 px-8 align-middle shadow-xl transition-all"
                )}
              >
                <div className="mb-3 flex items-center justify-between">
                  {props.title ? (
                    <Dialog.Title
                      as="h3"
                      className="-translate-y-1 text-2xl font-bold leading-6 text-font"
                    >
                      {props.title}
                    </Dialog.Title>
                  ) : (
                    <div />
                  )}
                  <Button
                    type="button"
                    icon="closeButton"
                    bigIcon
                    clear
                    onClick={props.onClose}
                  />
                </div>

                {props.children}
              </Dialog.Panel>
            </div>
          </div>
        </Transition.Child>
      </Dialog>
    </Transition>
  );
}