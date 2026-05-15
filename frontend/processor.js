class AudioProcessor extends AudioWorkletProcessor {
  process(inputs) {
    const input = inputs[0];

    if (input && input[0]) {
      const samples = input[0];
      this.port.postMessage(Array.from(samples));
    }

    return true;
  }
}

registerProcessor("audio-processor", AudioProcessor);