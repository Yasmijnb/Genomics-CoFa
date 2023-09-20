###########################################################################

# Genomics CoFa Job interview assessment
# Author: Yasmijn Balder

###########################################################################

# Load the packages
library(ggplot2)            # Used to make pretty plots

###########################################################################

# Import the read counts file
readcounts <- read.csv("../ReadCounts.csv", sep = ";", dec = ',')

# Order the data by sample names
ordered_QC <- readcounts[order(readcounts$SampleID), ]

# Make #NUM! into NA
ordered_QC[ordered_QC == "#NUM!"] <- NA

# Make sure the read counts are numeric
ordered_QC$ReadCount <- as.numeric(sub(",", ".", ordered_QC$ReadCount, fixed = TRUE))

# Isolated the controls
controls <- ordered_QC[292:320,]

# Add an explanatory control column
controls$ControlType <- c(rep('Negative DNA isolation control', 13), rep('Negative PCR control', 8), rep('Positive PCR control', 8))

# Create a plot of the filtered read count
ggplot(controls, aes(x = controls$SampleID, y=controls$ReadCount)) + 
  geom_point(aes(colour = controls$ControlType)) + 
  # Make plot black and white
  theme_bw() +
  # Change label names
  labs(x = "Controls", y = "Read counts") +
  # Rotate the x-axis labels
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) +
  # Remove the legend title
  theme(legend.title = element_blank()) + 
  # Add custom colours
  scale_color_manual(values=c("#56B4E9", "#D55E00", "#009E73"))

# Save the plot as png
ggsave('Controls.png')

       