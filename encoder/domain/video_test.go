package domain_test

import (
	"encoder/domain"
	"testing"
	"time"

	uuid "github.com/satori/go.uuid"
	"github.com/stretchr/testify/require"
)

func TestValidateIfVideoIsEmpty(t *testing.T) {
	video := domain.NewVideo()
	err := video.Validate()

	require.Error(t, err)
}

func TestVideoIdIsNotAUuid(t *testing.T) {
	video := domain.NewVideo()
	video.ID = "abc"
	video.ResourceId = "abc"
	video.FilePath = "abc"
	video.CreatedAt = time.Now()
	err := video.Validate()

	require.Error(t, err)
}

func TestVideoIsValid(t *testing.T) {
	video := domain.NewVideo()
	video.ID = uuid.NewV4().String()
	video.ResourceId = "abc"
	video.FilePath = "abc"
	video.CreatedAt = time.Now()
	err := video.Validate()

	require.Nil(t, err)
}
