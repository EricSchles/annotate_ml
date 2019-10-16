from .annotator import Annotator

def randomize_order(sample, num_samples):
    return [sample.sample(frac=1)
            for _ in range(num_samples)]

def reorder_by_index(annotated_samples):
    return [sample.sort_index(inplace=True)
            for sample in annotated_samples]

def annotate_samples(num_samples,
                     df,
                     n=None,
                     weights=None,
                     replace=False,
                     frac=None):
    sample = df.sample(
        n=n,
        weights=weights,
        replace=replace,
        frac=frac
    )
    samples = randomize_order(
        sample, num_samples
    )
    annotated_samples = []
    for sample in samples:
        annotated_sample = Annotator(sample).annotate()
        annotated_samples.append(
            annotated_sample
        )
    annotated_samples = reorder_by_index(
        annotated_samples
    )
    return annotated_samples

def analyze_annotations(annotated_samples, label):
    annotations_equivalent = []
    for index, sample in enumerate(annotated_samples[1:]):
        one = sample[label]
        two = annotated_samples[index][label]
        annotations_equivalent.append(
            one.equals(two)
        )
    print(
        "Are all annotations equal?",
        all(annotations_equivalent)
    )
    
    for index, sample in enumerate(annotated_samples[1:]):
        one = sample[label]
        two = annotated_samples[index][label]
        annotations_equivalent.append(
            one.equals(two)
        )
    
    
