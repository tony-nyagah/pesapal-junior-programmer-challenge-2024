package main

import (
	"bytes"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"hash/crc32"
	"os"
	"path/filepath"
	"strings"
)

// ------------------- PNG Handling -------------------

// insertChunkBeforeIEND inserts a custom ancillary chunk before the IEND chunk in a PNG file.
// This chunk can contain arbitrary data without affecting the displayed image.
func insertChunkBeforeIEND(data []byte, chunkType string, chunkData []byte) ([]byte, error) {
	// Find the IEND chunk in the PNG
	iendPos := findPNGChunk(data, "IEND")
	if iendPos < 0 {
		return nil, errors.New("IEND chunk not found in PNG")
	}

	// PNG chunk format:
	// length (4 bytes) + type (4 bytes) + data (length bytes) + CRC (4 bytes)
	length := len(chunkData)
	lengthBytes := toBigEndian(uint32(length))
	typeBytes := []byte(chunkType)

	// Compute CRC of type+data using IEEE CRC32
	crc := crc32.ChecksumIEEE(append(typeBytes, chunkData...))
	crcBytes := toBigEndian(crc)

	// Insert the chunk before IEND
	var buf bytes.Buffer
	buf.Write(data[:iendPos]) // all data before IEND
	buf.Write(lengthBytes)    // chunk length
	buf.Write(typeBytes)      // chunk type
	buf.Write(chunkData)      // chunk data
	buf.Write(crcBytes)       // chunk CRC
	buf.Write(data[iendPos:]) // the IEND chunk and what follows

	return buf.Bytes(), nil
}

// findPNGChunk finds the position of a chunk with the given type in the PNG data.
// Returns the offset to the start of the chunk length field, or -1 if not found.
func findPNGChunk(data []byte, chunkType string) int {
	// PNG signature is 8 bytes
	offset := 8
	for offset < len(data) {
		if offset+8 > len(data) {
			return -1
		}
		length := int(fromBigEndian(data[offset : offset+4]))
		ctype := string(data[offset+4 : offset+8])
		if ctype == chunkType {
			return offset
		}
		// Move to next chunk: length of data + 12 bytes overhead (4 length,4 type,4 CRC)
		offset += 12 + length
	}
	return -1
}

// ------------------- JPEG Handling -------------------

// insertCOMSegment inserts a COM (comment) segment after the SOI marker in a JPEG file.
// The COM segment won't affect the displayed image, allowing invisible changes.
func insertCOMSegment(jpegData []byte, comData []byte) ([]byte, error) {
	// Verify minimum structure: SOI (FF D8) at start and EOI (FF D9) at end
	if len(jpegData) < 4 || jpegData[0] != 0xFF || jpegData[1] != 0xD8 {
		return nil, errors.New("not a valid JPEG (no SOI)")
	}
	if jpegData[len(jpegData)-2] != 0xFF || jpegData[len(jpegData)-1] != 0xD9 {
		return nil, errors.New("not a valid JPEG (no EOI)")
	}

	// We'll insert the COM segment right after the SOI marker.
	// Segment format for COM:
	// FF FE [length-hi length-lo] [data...]
	// length includes these two length bytes, so length = dataLen + 2.

	length := len(comData) + 2
	comSegment := make([]byte, 4+len(comData))
	comSegment[0] = 0xFF
	comSegment[1] = 0xFE
	comSegment[2] = byte(length >> 8)
	comSegment[3] = byte(length & 0xFF)
	copy(comSegment[4:], comData)

	// Insert after SOI (2 bytes: FF D8)
	insertPos := 2

	newData := make([]byte, 0, len(jpegData)+len(comSegment))
	newData = append(newData, jpegData[:insertPos]...)
	newData = append(newData, comSegment...)
	newData = append(newData, jpegData[insertPos:]...)

	return newData, nil
}

// ------------------- Shared Utility Functions -------------------

// fromBigEndian interprets a 4-byte slice as a big-endian uint32.
func fromBigEndian(b []byte) uint32 {
	return uint32(b[0])<<24 | uint32(b[1])<<16 | uint32(b[2])<<8 | uint32(b[3])
}

// toBigEndian converts a uint32 to a 4-byte big-endian slice.
func toBigEndian(val uint32) []byte {
	b := make([]byte, 4)
	b[0] = byte((val >> 24) & 0xFF)
	b[1] = byte((val >> 16) & 0xFF)
	b[2] = byte((val >> 8) & 0xFF)
	b[3] = byte(val & 0xFF)
	return b
}

// hashFileData computes the SHA-256 hash of the given data and returns it as a hex string.
func hashFileData(data []byte) string {
	h := sha256.Sum256(data)
	return hex.EncodeToString(h[:])
}

// spoofFile reads the input file, determines if it is PNG or JPEG based on the extension,
// then repeatedly tries to modify it by inserting invisible data until the hash starts with 'prefix'.
func spoofFile(prefix, inputPath, outputPath string) error {
	inputData, err := os.ReadFile(inputPath)
	if err != nil {
		return fmt.Errorf("failed to read input file: %w", err)
	}

	// Print hash of the original input
	originalHexHash := hashFileData(inputData)
	fmt.Printf("Original file hash: %s  %s\n", originalHexHash, inputPath)

	// Determine file extension to handle image type
	ext := strings.ToLower(filepath.Ext(inputPath))
	isPNG := ext == ".png"
	isJPEG := ext == ".jpg" || ext == ".jpeg"

	if !isPNG && !isJPEG {
		return errors.New("unsupported file format (only PNG/JPG supported)")
	}

	// Begin brute force attempts
	attempt := 0
	for {
		attempt++

		// Generate random data to insert.
		// For PNG: We'll insert a custom chunk (type npFX).
		// For JPEG: We'll insert a COM segment.
		chunkData := make([]byte, 32) // 32 random bytes
		_, err := rand.Read(chunkData)
		if err != nil {
			return fmt.Errorf("failed to generate random data: %w", err)
		}

		var newData []byte
		if isPNG {
			// Check PNG signature
			if !bytes.HasPrefix(inputData, []byte("\x89PNG\r\n\x1a\n")) {
				return errors.New("invalid PNG file")
			}
			newData, err = insertChunkBeforeIEND(inputData, "npFX", chunkData)
			if err != nil {
				return fmt.Errorf("failed to insert PNG chunk: %w", err)
			}
		} else if isJPEG {
			// JPEG approach
			newData, err = insertCOMSegment(inputData, chunkData)
			if err != nil {
				return fmt.Errorf("failed to insert JPEG COM segment: %w", err)
			}
		}

		hexHash := hashFileData(newData)

		// Check if hash starts with the desired prefix
		if strings.HasPrefix(hexHash, prefix) {
			err = os.WriteFile(outputPath, newData, 0644)
			if err != nil {
				return fmt.Errorf("failed to write output file: %w", err)
			}
			fmt.Printf("Success after %d attempts!\n", attempt)
			fmt.Printf("Resulting hash: %s  %s\n", hexHash, outputPath)
			return nil
		}

		// Print progress every 1000 attempts for user feedback
		if attempt%1000 == 0 {
			fmt.Printf("Attempt %d: current hash prefix: %q\n", attempt, hexHash[:len(prefix)])
		}
	}
}

// ------------------- Main Function at the End -------------------

// main is the entry point.
// Usage: ./spoof <hex_prefix> <input_image> <output_image>
// Example: ./spoof 0x24 original.png altered.png
// This will attempt to find a file whose SHA-256 hash begins with "24".
func main() {
	if len(os.Args) < 4 {
		fmt.Fprintf(os.Stderr, "Usage: %s <hex_prefix> <input_image> <output_image>\n", os.Args[0])
		os.Exit(1)
	}

	prefix := os.Args[1]
	inputPath := os.Args[2]
	outputPath := os.Args[3]

	// Normalize prefix by removing "0x" if present
	prefix = strings.TrimPrefix(prefix, "0x")
	prefix = strings.ToLower(prefix)

	if err := spoofFile(prefix, inputPath, outputPath); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}
