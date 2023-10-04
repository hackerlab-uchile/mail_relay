import clsx from "clsx";
import Image from "next/image";
import _ from "lodash";
import { FaSpinner } from "react-icons/fa";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  filled?: boolean;
  clear?: boolean;
  icon?: string;
  disabled?: boolean;
  loading?: boolean;
  bigIcon?: boolean;
}

export default function Button(props: ButtonProps) {
  const { disabled, filled, clear, icon, loading, bigIcon } = props;
  return (
    <button
      {..._.omit(props, ["icon", "filled", "clear", "loading", "bigIcon"])}
      className={clsx(
        "h-10 rounded-lg border-primary text-sm tracking-wide",
        props.children ? "px-4" : "w-10",
        clear ? "border-none" : "border-2",
        filled ? "bg-primary text-white" : "text-primary",
        disabled && "opacity-50",
        props.className
      )}
    >
      {loading && props.children ? (
        <div className="flex items-center gap-3">
          <FaSpinner className="h-4 w-4 animate-spin" />
          <div>{props.children}</div>
        </div>
      ) : loading && !props.children ? (
        <FaSpinner className="m-auto h-4 w-4 animate-spin" />
      ) : icon && props.children ? (
        <div className="flex items-center gap-3">
          <Image
            src={`/icons/${icon}.svg`}
            width={16}
            height={16}
            alt=""
            className="h-4 w-4"
          />
          <div>{props.children}</div>
        </div>
      ) : icon && !props.children ? (
        <Image
          src={`/icons/${icon}.svg`}
          width={16}
          height={16}
          alt=""
          className={clsx("m-auto", bigIcon ? "h-8 w-8" : "h-4 w-4")}
        />
      ) : (
        props.children
      )}
    </button>
  );
}