package domain_test

import (
	"encoder/domain"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
)

func TestNewJob(t *testing.T) {
	video := domain.NewVideo()
	video.ID = "abc"
	video.ResourceId = "abc"
	video.FilePath = "abc"
	video.CreatedAt = time.Now()

	job, err := domain.NewJob("path", "Converted", video)

	require.Nil(t, err)
	require.NotNil(t, job)
}
