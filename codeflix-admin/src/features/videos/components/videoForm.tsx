import {
  Button,
  FormControl,
  FormLabel,
  Grid,
  RadioGroup,
  TextField,
} from "@mui/material";
import { Box } from "@mui/system";
import type { CastMember } from "../../../types/castMember";
import type { Category } from "../../../types/category";
import type { Genre } from "../../../types/genre";
import type { Video, FileObject } from "../../../types/videos";
import { Link } from "react-router";
import { AutoCompleteFields } from "../../../components/autoCompleteFields";
import type { FormEvent, ChangeEvent } from "react";
import { RatingsList } from "../../../components/ratingList";

type Props = {
  video: Video;
  genres?: Genre[];
  categories?: Category[];
  castMembers?: CastMember[];
  isDisabled?: boolean;
  isLoading?: boolean;
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
  changeHandler: (e: ChangeEvent<HTMLInputElement>) => void;
  handleAddFile: ({ name, file }: FileObject) => void;
  handleRemoveFile: (name: string) => void;
};

export default function VideosForm({
  video,
  genres,
  categories,
  castMembers,
  isDisabled = false,
  isLoading = false,
  onSubmit,
  changeHandler,
  handleAddFile,
  handleRemoveFile,
}: Props) {
  const handleAddThumbnail = (file: File) => {
    handleAddFile({ name: "thumb_file", file });
  };

  const handleRemoveThumbnail = () => {
    handleRemoveFile("thumb_file");
  };

  const handleAddBanner = (file: File) => {
    handleAddFile({ name: "banner_file", file });
  };

  const handleAddTrailer = (file: File) => {
    handleAddFile({ name: "trailer_file", file });
  };

  const handleAddVideo = (file: File) => {
    handleAddFile({ name: "video_file", file });
  };

  const handleRemoveBanner = () => {
    handleRemoveFile("banner_file");
  };

  const handleRemoveTrailer = () => {
    handleRemoveFile("trailer_file");
  };

  const handleRemoveVideo = () => {
    handleRemoveFile("video_file");
  };

  return (
    <Box p={2}>
      <form onSubmit={onSubmit}>
        <Grid container spacing={4}>
          <Grid
            size={{ xs: 12, md: 6 }}
            sx={{ "& .MuiTextField-root": { my: 2 } }}
          >
            <FormControl fullWidth>
              <TextField
                name="title"
                label="Title"
                data-testid="title"
                value={video.title}
                disabled={isDisabled}
                onChange={changeHandler}
              />
            </FormControl>
            <FormControl fullWidth>
              <TextField
                multiline
                minRows={4}
                name="description"
                label="Description"
                data-testid="description"
                disabled={isDisabled}
                onChange={changeHandler}
                value={video.description}
              />
            </FormControl>

            <Grid container spacing={2}>
              <Grid size={{ xs: 6 }}>
                <FormControl fullWidth>
                  <TextField
                    name="year_launched"
                    label="Year Launched"
                    data-testid="year_launched"
                    disabled={isDisabled}
                    onChange={changeHandler}
                    value={video.year_launched}
                  />
                </FormControl>
              </Grid>
              <Grid size={{ xs: 6 }}>
                <FormControl fullWidth>
                  <TextField
                    name="duration"
                    label="Duration"
                    data-testid="duration"
                    disabled={false}
                    value={video.duration}
                    onChange={changeHandler}
                  />
                </FormControl>
              </Grid>
            </Grid>

            <Grid size={{ xs: 12 }}>
              <AutoCompleteFields
                name="cast_members"
                label="Cast Members"
                isLoading={isLoading}
                isDisabled={isDisabled}
                values={video.cast_members}
                options={castMembers}
                changeHandler={changeHandler}
              />
            </Grid>

            <Grid size={{ xs: 12 }}>
              <Grid
                container
                alignContent={"center"}
                justifyContent={"space-between"}
                spacing={2}
              >
                <Grid size={{ xs: 5 }}>
                  <AutoCompleteFields
                    name="genres"
                    label="Genres"
                    isLoading={isLoading}
                    isDisabled={isDisabled}
                    values={video.genres}
                    options={genres}
                    changeHandler={changeHandler}
                  />
                </Grid>

                <Grid size={{ xs: 5 }}>
                  <AutoCompleteFields
                    name="categories"
                    label="Categories"
                    isLoading={isLoading}
                    isDisabled={false}
                    values={video.categories}
                    options={categories}
                    changeHandler={changeHandler}
                  />
                </Grid>
              </Grid>
            </Grid>
          </Grid>
          <Grid
            size={{ xs: 12, md: 6 }}
            sx={{ "& .MuiTextField-root": { my: 2 } }}
          >
            <FormControl fullWidth>
              <Box mt={2} mb={2}>
                <FormLabel component="legend">Rating</FormLabel>
              </Box>
              <RadioGroup
                row
                name="rating"
                value={video.rating}
                onChange={changeHandler}
              >
                <RatingsList isDisabled={isDisabled} />
              </RadioGroup>
            </FormControl>

            <FormControl fullWidth>
              <InputFile
                onAdd={handleAddThumbnail}
                onRemove={handleRemoveThumbnail}
                placeholder="Thumbnail"
                data-testid="thumbnail-input"
              />
              <InputFile
                onAdd={handleAddBanner}
                onRemove={handleRemoveBanner}
                placeholder="Banner"
                data-testid="banner-input"
              />
            </FormControl>

            <FormControl fullWidth>
              <InputFile
                onAdd={handleAddVideo}
                onRemove={handleRemoveVideo}
                placeholder="Video"
                data-testid="video-input"
              />
              <InputFile
                onAdd={handleAddTrailer}
                onRemove={handleRemoveTrailer}
                placeholder="Trailer"
                data-testid="trailer-input"
              />
            </FormControl>
          </Grid>
        </Grid>

        <Box display="flex" sx={{ my: 2 }} gap={2}>
          <Button variant="contained" component={Link} to="/videos">
            Back
          </Button>

          <Button
            type="submit"
            color="secondary"
            variant="contained"
            disabled={isDisabled || isLoading}
          >
            {isLoading ? "Loading..." : "Save"}
          </Button>
        </Box>
      </form>
    </Box>
  );
}
