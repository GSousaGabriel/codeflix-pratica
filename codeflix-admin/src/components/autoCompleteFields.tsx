import {
  Autocomplete,
  type AutocompleteRenderInputParams,
  TextField,
} from "@mui/material";
import type { CastMember } from "../types/castMember";
import type { Category } from "../types/category";
import type { Genre } from "../types/genre";
import type { ChangeEvent, HTMLAttributes } from "react";

type Props = {
  name: string;
  label: string;
  isLoading: boolean;
  isDisabled: boolean;
  values?: (Genre | Category | CastMember)[];
  options?: (Genre | Category | CastMember)[];
  changeHandler: (e: ChangeEvent<HTMLInputElement>) => void;
};

export const AutoCompleteFields = ({
  name,
  label,
  values,
  options,
  isLoading,
  isDisabled,
  changeHandler,
}: Props) => {
  const renderOptions = (
    props: HTMLAttributes<HTMLLIElement>,
    option: Category | Genre | CastMember
  ) => (
    <li {...props} key={option.id}>
      {option.name}
    </li>
  );

  const isEqualId = (
    option: Genre | Category | CastMember,
    value: Genre | Category | CastMember
  ) => {
    return option.id === value.id;
  };

  const handleOnChange = (
    _e: ChangeEvent<{}>,
    newValue: (Genre | Category | CastMember)[]
  ) => {
    changeHandler({ target: { name, value: newValue } } as any);
  };

  const renderInput = (params: AutocompleteRenderInputParams) => (
    <TextField {...params} label={label} data-testid={`${name}-input`} />
  );

  return (
    <Autocomplete
      multiple
      value={values}
      options={options || []}
      loading={isLoading}
      onChange={handleOnChange}
      renderInput={renderInput}
      data-testid={`${name}-search`}
      renderOption={renderOptions}
      isOptionEqualToValue={isEqualId}
      disabled={isDisabled || !options}
      getOptionLabel={(option) => option.name}
    />
  );
};