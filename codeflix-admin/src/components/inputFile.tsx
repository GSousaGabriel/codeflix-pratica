import { IconButton, TextField } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import FileIcon from "@mui/icons-material/FileCopy";
import { useRef, useState, type ChangeEvent } from "react";

interface Props {
  onAdd: (file: File) => void;
  onRemove: (file: File) => void;
  placeholder: string;
}

const InputFile = ({ onAdd, onRemove, placeholder }: Props) => {
  const [selectedFile, setSelectedFile] = useState<File | null>();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const onAddHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files ? e.target.files[0] : undefined;
    if (!file) return;
    setSelectedFile(file);
    onAdd(file);
  };

  const onRemoveHandler = () => {
    setSelectedFile(undefined);
    if (selectedFile) {
      onRemove(selectedFile);
    }
  };

  const handleFileInput = () => {
    if (fileInputRef) {
      fileInputRef.current?.click();
    }
  };

  return (
    <>
      <TextField
        type="text"
        placeholder={placeholder}
        aria-readonly
        value={selectedFile?.name || ""}
        slotProps={{
          input: {
            endAdornment: selectedFile ? (
              <IconButton onClick={onRemoveHandler}>
                <DeleteIcon />
              </IconButton>
            ) : (
              <IconButton onClick={handleFileInput}>
                <FileIcon />
              </IconButton>
            ),
            readOnly: true,
          },
        }}
      />
      <input
        ref={fileInputRef}
        type="file"
        id="inputFile"
        data-testid="inputFile"
        accept="*"
        style={{ display: "none" }}
        onChange={onAddHandler}
      />
    </>
  );
};

export default InputFile;
